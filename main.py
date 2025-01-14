import searxng

if __name__ == "__main__":
    api = searxng.SearXNG("https://search.vtallen.com")

    responses = api.search_n("xbox series x", 5)

    print(f"Found {len(responses)} links")
    print("==============================================")
    print()
    for response in responses:
        print(str(response))
