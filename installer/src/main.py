# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# export PYTHONPATH="/Users/nyanyacyan/Desktop/project_file/LGRAM_auto_processer/installer/src"

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import asyncio

# flow
from method.flow import SingleProcess


# ----------------------------------------------------------------------------------
# **********************************************************************************

class Main:

    async def main(self):
        main_flow = SingleProcess()
        await main_flow._single_process()

# **********************************************************************************

if __name__ == "__main__":
    asyncio.run(Main().main())

# ----------------------------------------------------------------------------------
