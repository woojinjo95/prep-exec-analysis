from sub.block import calc_scenario_to_run_blocks, calc_analysis_to_run_blocks
from sub.state import set_run_state, set_analysis_state


async def setup_playblock(state: dict, db_scenario: any, db_blocks: any, conn: any):
    testrun_id = state.get('id')
    scenario_id = state.get('scenario_id')
    scenario = db_scenario.find_one({'id': scenario_id})
    total_loop = scenario.get('repeat_cnt') if hasattr(scenario, 'repeat_cnt') else 1
    blocks = calc_scenario_to_run_blocks(total_loop, scenario)

    # 수행할 때마다 테스트런이 증가해야 하지만 현재 증가하지 않으므로 임시로 upsert 사용
    db_blocks.update_one({
        "testrun": testrun_id,
        "scenario": scenario_id,
    }, {'$set': {
        "blocks": blocks
    }}, upsert=True)

    # 동작 상태를 run으로 설정함
    await set_run_state(conn)


async def setup_analysis(state: dict, db_scenario: any, db_blocks: any, conn: any):
    testrun_id = state.get('id')
    scenario_id = state.get('scenario_id')
    # scenario_id = '3201ba8a-b96d-4b11-9298-35cdee3eb476'
    # testrun_id = '2023-09-01T065554F133036'
    pipeline = [{"$match": {'id': scenario_id}},
                {"$unwind": "$testruns"},
                {"$project": {"testrun_id": "$testruns.id",
                            "config": "$testruns.analysis.config"}},
                {"$match": {"testrun_id": testrun_id}},
                {"$project": {"_id": 0, "config": "$config"}}]
    
    analysis_configs = list(db_scenario.aggregate(pipeline))

    blocks = calc_analysis_to_run_blocks(analysis_configs[0]['config'])
    # print(blocks)
    # 수행할 때마다 테스트런이 증가해야 하지만 현재 증가하지 않으므로 임시로 upsert 사용
    db_blocks.update_one({
        "testrun": "analysis",
        "scenario": "analysis",
    }, {'$set': {
        "blocks": blocks
    }}, upsert=True)

    # 동작 상태를 run으로 설정함
    await set_analysis_state(conn)
