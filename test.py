from getImage import a_check_urls_parallel_inner, getImage
import asyncio

URLs = getImage('A7223-0002', '', True)

async def main(URLs):
    result = await a_check_urls_parallel_inner(URLs)
    print("Valid URLs:", result)
    return result

if __name__ == "__main__":
    print(asyncio.run(main(URLs)))

