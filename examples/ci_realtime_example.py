import asyncio
from pyguardian.ci_realtime import Broadcaster


async def main():
    bc = Broadcaster()
    await bc.start()
    await asyncio.sleep(0.1)
    payload = {"cost": {"health_score": 92.0}, "gate": {"threshold": 80.0, "fail": False}}
    ok = await bc.publish(payload)
    print({"published": ok})


if __name__ == "__main__":
    asyncio.run(main())
