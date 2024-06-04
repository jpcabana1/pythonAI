
# Patterns Example
from common.Patterns.Factory.AnimalFactory import AnimalFactory

if __name__ == "__main__":
    print(AnimalFactory().create("Cat").speak())


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