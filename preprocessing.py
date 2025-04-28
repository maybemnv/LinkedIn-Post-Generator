import json
import re
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


json_paser=JsonOutputParser()
def process_posts(raw_file_path, processed_file_path=None):
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        enriched_posts = []
        for post in posts:
            metadata = extract_metadata(post.get('text', ''))  # Use .get() to avoid KeyError
            post_with_metadata = {**post, **metadata}  # Use dictionary unpacking for merging
            enriched_posts.append(post_with_metadata)

    unified_tags = get_unified_tags(enriched_posts)
    for post in enriched_posts:
        current_tags = post.get('tags', [])  # Use .get() to avoid KeyError
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}  # Handle missing tags in unified_tags
        post['tags'] = list(new_tags)

    if not processed_file_path:
        raise ValueError("Processed file path is required.")  # Validate processed_file_path

    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)

def extract_metadata(post):
    template = '''
    You are given a LinkedIn post. You need to extract number of lines, language of the post and tags.
    1. Return a valid JSON. No preamble.
    2. JSON object should have exactly three keys: line_count, language and tags.
    3. tags is an array of text tags. Extract maximum two tags.
    4. Language should be English or Hinglish (Hinglish means hindi + english)

    Here is the actual post on which you need to perform this task:  
    {post}
    '''

    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke({"post": post})

    # Try parsing only the valid JSON block
    try:
        json_parser = JsonOutputParser()
        return json_parser.parse(response.content)
    except Exception:
        try:
            json_block = re.search(r"\{[\s\S]*\}", response.content)
            if json_block:
                return json.loads(json_block.group())
            else:
                raise ValueError("No JSON block found.")
        except Exception as e:
            raise OutputParserException(f"Error parsing metadata: {str(e)}")
def get_unified_tags(posts_with_metadata):
    unique_tags = set()
    # Loop through each post and extract the tags
    for post in posts_with_metadata:
        unique_tags.update(post.get('tags', []))  # Use .get() to avoid KeyError

    unique_tags_list = ','.join(unique_tags)

    template = '''Return ONLY a JSON object that maps tags to their unified versions.
    Requirements:
    1. Tags should be unified and merged to create a shorter list
    2. Each tag should follow title case convention
    3. NO text before or after the JSON object
    4. NO explanation, just the JSON object
    
    Example output:
    {{"Jobseekers": "Job Search", "Job Hunting": "Job Search", "Motivation": "Motivation"}}
    
    Tags to unify: {tags}
    '''
    
    pt = PromptTemplate.from_template(template)
    response = None  # Initialize response variable
    try:
        chain = pt | llm
        response = chain.invoke(input={"tags": unique_tags_list})
        # Add pre-processing to clean the response
        json_str = response.content.strip()
        if json_str.startswith('```json'):
            json_str = json_str[7:]
        if json_str.endswith('```'):
            json_str = json_str[:-3]
        json_str = json_str.strip()
        
        json_parser = JsonOutputParser()
        res = json_parser.parse(json_str)
        return res
    except Exception as e:
        error_msg = f"Error parsing tags response: {str(e)}"
        if response:
            error_msg += f"\nResponse was: {response.content}"
        raise OutputParserException(error_msg)
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw_posts.json", help="Path to the raw posts file")
    parser.add_argument("--output", default="data/processed_posts.json", help="Path to the processed posts file")
    args = parser.parse_args()
    process_posts(args.input, args.output)