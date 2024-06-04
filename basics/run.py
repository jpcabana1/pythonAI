import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    secret_key = os.getenv("SECRET_KEY")
    database_url = os.getenv("DATABASE_URL")
    debug_mode = os.getenv("DEBUG")

    print(f"Secret Key: {secret_key}")
    print(f"Database URL: {database_url}")
    print(f"Debug Mode: {debug_mode}")

if __name__ == "__main__":
    main()

'''
#Asyncio Example
import asyncio

async def await_for(time: int) -> str:
    await asyncio.sleep(time)
    return f"Finished {time}s."

async def main():
   gather_return = await asyncio.gather(
        await_for(4),
        await_for(5)
    )
   print(gather_return[1])

if __name__ == "__main__":
    asyncio.run(main())
'''

'''
# Patterns Example
from common.Patterns.Factory.AnimalFactory import AnimalFactory

if __name__ == "__main__":
    print(AnimalFactory().create("Cat").speak())
'''



