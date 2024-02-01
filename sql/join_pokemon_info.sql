SELECT
  p.* EXCEPT (_airbyte_raw_id,
    _airbyte_extracted_at,
    _airbyte_meta),
  i.name AS ingredient,
  i.energy AS ingredient_energy,
  f.name AS fruit,
  f.lv60_energy AS fruit_energy,
  m.name AS main_skill,
  m.Lv1,
  m.Lv2,
  m.Lv3,
  m.Lv4,
  m.Lv5,
  m.Lv6,
FROM
  `PokemonSleep.Pokemon` AS p
JOIN
  `PokemonSleep.Ingredient` AS i
ON
  i.name = p.ingredient
JOIN
  `PokemonSleep.Fruit` AS f
ON
  f.name = p.fruit
JOIN
  `PokemonSleep.MainSkill` AS m
ON
  m.name = p.main_skill