import numpy as np
from pymongo.mongo_client import MongoClient

# 2023.09.28 更新為「寶可夢Sleep潛力計算機v4.0」版本

def calculator(
        uri, 
        pokemon, 
        main_skill, 
        nature, 
        sub_skills, 
        ingredient_2,
        ingredient_num_2,
        ingredient_3,
        ingredient_num_3
    ):

    # Database connection
    client = MongoClient(uri)
    db = client['PokemonSleep']
    natures_collection = db['Nature']
    pokemon_collection = db['Pokemon']
    mainSkill_collection = db['MainSkill']
    # sub_skill_collection = db['SubSkill']
    fruit_collection = db['Fruit']
    ingredient_collection = db['Ingredient']

    # Pokemon
    pokemon_info = pokemon_collection.find_one(pokemon)
    final_help_interval = pokemon_info['final_help_interval']
    final_evolution_step = pokemon_info['final_evolution_step']
    carry_limit = pokemon_info['carry_limit']
    fruit_type = pokemon_info['type'] 

    # Fruit
    fruit_energy = fruit_collection.find_one(pokemon_info['fruit'])['energy']

    pokemon_info = pokemon_collection.find_one(pokemon)

    # 食材均能計算
    ingredient_energy_1 = ingredient_collection.find_one(pokemon_info['ingredient'])['energy']
    ingredient_num_1 = pokemon_info['ingredient_num']
    ingredient_energy_total_1 = ingredient_num_1 * ingredient_energy_1
    ingredient_energy_2 = ingredient_collection.find_one(ingredient_2)['energy']
    ingredient_energy_total_2 = ingredient_num_2 * ingredient_energy_2
    ingredient_energy_3 = ingredient_collection.find_one(ingredient_3)['energy']
    ingredient_energy_total_3 = ingredient_num_3 * ingredient_energy_3
    ingredient_energy_avg = sum(
            [ingredient_energy_total_1, ingredient_energy_total_2, ingredient_energy_total_3]
        )/3

    # MainSkill
    main_skill_basic_energy = mainSkill_collection.find_one(main_skill)['energy']

    # Nature
    nature = natures_collection.find_one(nature)
    nature_up = nature['up']
    nature_down = nature['down']

    # 幫忙間隔
    def calculate_help_interval():
        helper_bonus = len([s for s in sub_skills if s == '幫手獎勵']) * 0.15
        help_speed_s = len([s for s in sub_skills if s == '幫忙速度S']) * 0.07
        help_speed_m = len([s for s in sub_skills if s == '幫忙速度M']) * 0.14

        nature_boost_up = 0.1 if nature_up == '幫忙速度' else 0
        nature_boost_down = -0.1 if nature_down == '幫忙速度' else 0
        nature_boost = nature_boost_up + nature_boost_down

        # 活力加速
        health_boost_up = 0.1 if nature_up == '活力回復' else 0
        health_boost_down = -0.1 if nature_down == '活力回復' else 0
        health_boost_sub = len([s for s in sub_skills if s == '活力回復獎勵']) * 0.02
        health_boost = health_boost_up + health_boost_down + health_boost_sub

        help_interval_param =  1 - (helper_bonus + help_speed_s + help_speed_m + nature_boost + health_boost + main_skill_health_boost + 59*0.002)
        calc_help_interval = final_help_interval * help_interval_param if help_interval_param > 0 else 1
        return calc_help_interval

    def calculate_main_skill_level_speed_param_health_boost():
        
        # 技能等級
        skill_level_s = len([s for s in sub_skills if s == '技能等級提升S'])
        skill_level_m = len([s for s in sub_skills if s == '技能等級提升M']) * 2
        skill_level = skill_level_s + skill_level_m

        # 主技能速度參數
        skill_speed_param_s = len([s for s in sub_skills if s == '技能機率提升S']) * 0.18
        skill_speed_param_m = len([s for s in sub_skills if s == '技能機率提升M']) * 0.36
        skill_speed_param_up = 0.2 if nature_up == '主技能' else 0
        skill_speed_param_down = -0.2 if nature_down == '主技能' else 0
        skill_speed_param = skill_speed_param_s + skill_speed_param_m + skill_speed_param_up + skill_speed_param_down

        # 主技活力加速
        final_skill_level = final_evolution_step + skill_level
        final_skill_speed_param = 1 + skill_speed_param
        main_skill_health_boost = (
            final_skill_level * 0.015 * final_skill_speed_param
            if main_skill in ['活力填充S', '活力療癒S', '活力全體療癒S'] 
            else 0
        )

        # 主技能能量
        main_skill_has_energy = (
            1 if main_skill not in ['活力填充S', '活力療癒S', '活力全體療癒S'] 
            else 0
        )
        
        main_skill_energy = main_skill_basic_energy['lv'+str(final_skill_level)] * main_skill_has_energy * final_skill_speed_param
        return main_skill_health_boost, main_skill_energy

    # 幫忙均能/次
    def calculate_avg_energy_per_help():
        
        # 食材機率
        ingredient_prob_s = len([s for s in sub_skills if s == '食材機率提升S']) * 0.18
        ingredient_prob_m = len([s for s in sub_skills if s == '食材機率提升M']) * 0.36
        ingredient_prob_up = 0.2 if nature_up == '食材發現' else 0
        ingredient_prob_down = -0.2 if nature_down == '食材發現' else 0
        ingredient_prob = 1 + ingredient_prob_s + ingredient_prob_m + ingredient_prob_up + ingredient_prob_down

        # 樹果能量
        fruit_num_by_type = 2 if fruit_type == '樹果型' else 1
        fruit_num_by_subskill = len([s for s in sub_skills if s == '樹果數量S'])
        final_fruit_num = fruit_num_by_type + fruit_num_by_subskill
        final_fruit_energy = final_fruit_num * fruit_energy
        avg_energy_per_help = round(ingredient_energy_avg * ingredient_prob + final_fruit_energy * (5-ingredient_prob))/5
        return final_fruit_num, ingredient_prob, avg_energy_per_help

    def calculate_carry_over_limit_energy(ingredient_prob, avg_energy_per_help, final_fruit_num, calc_help_interval):
        # 持有上限溢出數
        ingredient_create_num = (ingredient_num_1 + ingredient_num_2 + ingredient_num_3)/3 * ingredient_prob
        fruit_create_num = (5 - ingredient_prob) * final_fruit_num
        carry_s = len([s for s in sub_skills if s == '持有上限提升S']) * 6
        carry_m = len([s for s in sub_skills if s == '持有上限提升M']) * 12
        carry_l = len([s for s in sub_skills if s == '持有上限提升L']) * 18
        carry_over_limit_num = (ingredient_create_num + fruit_create_num) * round(30600/calc_help_interval) - (carry_limit + carry_s + carry_m + carry_l)
        
        # 持有上限溢出能量
        carry_over_limit_energy_param = carry_over_limit_num * (ingredient_prob/5) if carry_over_limit_num * avg_energy_per_help > 0 else 0
        avg_energy_per_ingredient = (ingredient_energy_1 + ingredient_energy_2 + ingredient_energy_3)/3
        carry_over_limit_energy = carry_over_limit_energy_param * avg_energy_per_ingredient / 3
        return carry_over_limit_energy

    def calculate_energy_score(calc_help_interval, avg_energy_per_help, carry_over_limit_energy):
        # 睡眠EXP獎勵
        sleep_exp_bonus = len([s for s in sub_skills if s == '睡眠EXP獎勵']) * 1000

        # 夢之碎片獎勵
        dream_stone_bonus = len([s for s in sub_skills if s == '夢之碎片獎勵']) * 500
        
        energy_score = round(
            (60000/calc_help_interval) * avg_energy_per_help + \
            main_skill_energy - \
            carry_over_limit_energy + \
            sleep_exp_bonus + \
            dream_stone_bonus
        )
        return energy_score

    def calculate_rank(energy_score):
        score_bins = [0, 6000, 7000, 8000, 9000, 10000, 12000, 14000, 999999999999]
        rank_dict = {
            1: 'E', 
            2: 'D', 
            3: 'C', 
            4: 'B', 
            5: 'A', 
            6: 'S', 
            7: 'SS', 
            8: 'SSS'
        }
        rank_num = np.digitize(energy_score, score_bins)
        return rank_dict[rank_num]

    main_skill_health_boost, main_skill_energy = calculate_main_skill_level_speed_param_health_boost()
    calc_help_interval = calculate_help_interval()
    final_fruit_num, ingredient_prob, avg_energy_per_help = calculate_avg_energy_per_help()
    carry_over_limit_energy = calculate_carry_over_limit_energy(ingredient_prob, avg_energy_per_help, final_fruit_num, calc_help_interval)
    energy_score = calculate_energy_score(calc_help_interval, avg_energy_per_help, carry_over_limit_energy)
    rank = calculate_rank(energy_score)
    return energy_score, rank
    
