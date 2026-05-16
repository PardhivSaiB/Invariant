import httpx
import re
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup

class LeetCodeService:
    def __init__(self):
        self.graphql_url = "https://leetcode.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _extract_slug(self, url: str) -> Optional[str]:
        match = re.search(r"problems/([^/]+)", url)
        return match.group(1) if match else None

    async def fetch_problem(self, url: str) -> Dict[str, Any]:
        slug = self._extract_slug(url)
        if not slug:
            raise ValueError("Invalid LeetCode URL")

        query = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            title
            content
            difficulty
            topicTags {
              name
            }
          }
        }
        """
        variables = {"titleSlug": slug}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.graphql_url,
                json={"query": query, "variables": variables},
                headers=self.headers
            )
            response.raise_for_status()
            data = response.json()

        if "data" not in data or "question" not in data["data"] or not data["data"]["question"]:
            raise ValueError(f"Problem not found for slug: {slug}")

        question = data["data"]["question"]
        title = question["title"]
        content_html = question["content"]
        difficulty = question["difficulty"]
        topic_tags = [tag["name"] for tag in question["topicTags"]]

        # Parse content HTML
        parsed_content = self._parse_content(content_html)

        return {
            "title": title,
            "description": parsed_content["description"],
            "constraints": parsed_content["constraints"],
            "examples": parsed_content["examples"],
            "difficulty": difficulty,
            "topic_tags": topic_tags,
            "url": url
        }

    def _parse_content(self, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, "html.parser")
        
        description_parts = []
        examples = []
        constraints = []

        # Find all example headers
        example_headers = soup.find_all(string=re.compile(r"Example \d+:"))
        
        # 1. Extract Description
        # We find the first example header and take everything before its top-level parent
        if example_headers:
            first_header = example_headers[0]
            # Find the highest parent that is still a direct child of soup or a main container
            target = first_header
            while target.parent and target.parent != soup:
                target = target.parent
            
            for element in soup.contents:
                if element == target:
                    break
                if hasattr(element, 'get_text'):
                    text = element.get_text().strip()
                    if text:
                        description_parts.append(text)
        else:
            description_parts.append(soup.get_text().strip())

        # 2. Extract Examples
        for header in example_headers:
            # Look for the nearest <pre> tag after this header
            pre_tag = header.find_next("pre")
            
            # Verify this <pre> belongs to THIS example (it's before the next example header)
            next_header = header.find_next(string=re.compile(r"Example \d+:"))
            
            # If there's a next header, the <pre> must be before it
            is_valid_pre = False
            if pre_tag:
                if not next_header:
                    is_valid_pre = True
                else:
                    # Crude check: is the pre_tag before next_header in the document?
                    # We can use find_all and check indices if needed, but usually it's immediate
                    curr = header.next_element
                    while curr and curr != next_header:
                        if curr == pre_tag:
                            is_valid_pre = True
                            break
                        curr = curr.next_element

            if is_valid_pre and pre_tag:
                example_text = pre_tag.get_text().strip()
                
                # Simple parse of Input/Output/Explanation
                input_match = re.search(r"Input:\s*(.*?)(?=\nOutput:|$)", example_text, re.DOTALL)
                output_match = re.search(r"Output:\s*(.*?)(?=\nExplanation:|$)", example_text, re.DOTALL)
                explanation_match = re.search(r"Explanation:\s*(.*)", example_text, re.DOTALL)

                examples.append({
                    "input": input_match.group(1).strip() if input_match else "",
                    "output": output_match.group(1).strip() if output_match else "",
                    "explanation": explanation_match.group(1).strip() if explanation_match else ""
                })

        # 3. Extract Constraints
        constraints_header = soup.find(string=re.compile(r"Constraints:"))
        if constraints_header:
            ul_tag = constraints_header.find_next("ul")
            if ul_tag:
                constraints = [li.get_text().strip() for li in ul_tag.find_all("li")]
            else:
                p_tag = constraints_header.find_next("p")
                if p_tag:
                    constraints = [p_tag.get_text().strip()]

        return {
            "description": "\n".join(description_parts).strip(),
            "examples": examples,
            "constraints": constraints
        }
