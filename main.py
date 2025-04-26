# server.py
from mcp.server.fastmcp import FastMCP
from Bio import Entrez
import yaml
import json


# Create an MCP server
mcp = FastMCP("PubMed")

with open("config.yaml", "r") as stream:
    try:
        PARAM = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

@mcp.tool()
def query_pubmed(my_search_term: str, limit: int = 3) -> list:
    """find related articles in PubMed"""

    Entrez.email = PARAM["email"]
    Entrez.api_key = PARAM["ncbi_key"]
    stream = Entrez.esearch(db="pubmed", term=my_search_term, retmax=limit, sort="pub_date")
    record = Entrez.read(stream)

    articles = []
    for r in record["IdList"]:

        stream_doc = Entrez.efetch(db="pubmed", id=r)
        record_doc = Entrez.read(stream_doc)
        for doc in record_doc["PubmedArticle"]:
            try:
                article = {}

                article["pubmed_id"] = r
                article["title"] = doc["MedlineCitation"]["Article"]["ArticleTitle"]

                article["abstract"] = doc["MedlineCitation"]["Article"]["Abstract"]["AbstractText"][0]

                #print (doc["MedlineCitation"]["Article"]["ArticleDate"][0])

                article["date"] = f'{doc["MedlineCitation"]["Article"]["ArticleDate"][0]["Year"]}.{doc["MedlineCitation"]["Article"]["ArticleDate"][0]["Month"]}.{doc["MedlineCitation"]["Article"]["ArticleDate"][0]["Day"]}'
                authors = []
                for author in doc["MedlineCitation"]["Article"]["AuthorList"]:
                    authors.append(author["LastName"] + " " + author["ForeName"])
                #print (doc["MedlineCitation"]["Article"]["AuthorList"][0])
                article["authors"] = authors
                article["journal"] = doc["MedlineCitation"]["Article"]["Journal"]["Title"]

                articles.append(article)
                #print (article)
            except:
                pass
    return (articles)


if __name__ == "__main__":
    print("Starting server...")
    # Initialize and run the server

    #print (query_pubmed("keytruda", 5))

    mcp.run(transport="stdio")