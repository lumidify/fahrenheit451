def borders(left, right, *args):
    if not args:
        return [-left / 2, left / 2, -right / 2, right / 2]
    else:
        return [left, right, args[0], args[1]]

obstacles = [
    {"images": "iso_tree_stump.png",
    "borders": borders(0.60, 0.60)},
    
    {"images": "iso_wall_grey_ns.png",
    "borders": borders(0.40, 1.10)},
    
    {"images": "iso_wall_grey_ew.png",
    "borders": borders(1.10, 0.40)},
    
    {"images": "iso_wall_grey_handle_ns.png",
    "borders": borders(0.40, 1.10)},
    
    {"images": "iso_wall_grey_handle_ew.png",
    "borders": borders(1.10, 0.40)},
    
    {"images": "iso_tree_big.png",
    "borders": borders(1.30, 1.30)},
    
    {"images": ["iso_door_unlocked_closed_we_1.png", "iso_door_unlocked_opened_we_2.png", "iso_door_unlocked_opened_we_3.png", "iso_door_unlocked_opened_we_4.png", "iso_door_unlocked_opened_we_5.png"],
    "animation": "door",
    "fps": 10},
    
    {"images": ["iso_door_unlocked_closed_ns_1.png", "iso_door_unlocked_opened_ns_2.png", "iso_door_unlocked_opened_ns_3.png", "iso_door_unlocked_opened_ns_4.png", "iso_door_unlocked_opened_ns_5.png"],
    "animation": "door",
    "fps": 10},

    {"images": ["iso_purplecloud_3.png", "iso_purplecloud_4.png", "iso_purplecloud_5.png", "iso_purplecloud_1.png", "iso_purplecloud_2.png"],
    "fps": 10},

    {"images": ["iso_teleport_1.png", "iso_teleport_2.png", "iso_teleport_3.png", "iso_teleport_4.png", "iso_teleport_5.png"],
    "fps": 10},

    {"images": ["iso_droidnest_red_1.png", "iso_droidnest_red_2.png", "iso_droidnest_red_3.png", "iso_droidnest_red_4.png", "iso_droidnest_red_5.png"],
    "fps": 5},

    {"images": ["iso_droidnest_blue_1.png", "iso_droidnest_blue_2.png", "iso_droidnest_blue_3.png", "iso_droidnest_blue_4.png", "iso_droidnest_blue_5.png"],
    "fps": 1},

    {"images": ["iso_droidnest_yellow_1.png", "iso_droidnest_yellow_2.png", "iso_droidnest_yellow_3.png", "iso_droidnest_yellow_4.png", "iso_droidnest_yellow_5.png"],
    "fps": 14},
    
    {"images": ["iso_droidnest_green_1.png", "iso_droidnest_green_2.png", "iso_droidnest_green_3.png", "iso_droidnest_green_4.png", "iso_droidnest_green_5.png"],
    "fps": 3},

    {"images": "floor_tiles/iso_collapsingfloor_visible.png",
    "borders": borders(0.00, 0.00)},

    {"images": "iso_trapdoor_w.png"},

    {"images": "iso_trapdoor_n.png"},

    {"images": "iso_door_locked_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_door_locked_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_chest_grey_closed_n.png",
    "label": "Chest",
    "borders": borders(0.80, 0.60),
    "action": "chest",
    "after_looting": 21},

    {"images": "iso_chest_grey_closed_w.png",
    "label": "Chest",
    "borders": borders(0.60, 0.80),
    "action": "chest",
    "after_looting": 22},

    {"images": "iso_chest_grey_opened_n.png",
    "borders": borders(0.80, 0.60)},

    {"images": "iso_chest_grey_opened_w.png",
    "borders": borders(0.60, 0.80)},

    {"images": "iso_autogun_on_w.png",
    "borders": borders(0.70, 0.70),
    "animation": "autogun"},

    {"images": "iso_autogun_on_n.png",
    "borders": borders(0.70, 0.70),
    "animation": "autogun"},

    {"images": "iso_autogun_on_e.png",
    "borders": borders(0.70, 0.70),
    "animation": "autogun"},

    {"images": "iso_autogun_on_s.png",
    "borders": borders(0.70, 0.70),
    "animation": "autogun"},

    {"images": "iso_wall_cave_we.png",
    "borders": borders(1.50, 1.00)},

    {"images": "iso_wall_cave_ns.png",
    "borders": borders(1.00, 1.50)},

    {"images": "iso_wall_cave_curve_ws.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_cave_curve_nw.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_cave_curve_es.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_cave_curve_ne.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_pot.png",
    "borders": borders(0.50, 0.50)},
    
    {"images": "iso_terminal_s.png",
    "label": "Terminal",
    "borders": borders(0.80, 0.80),
    "action": "terminal"},

    {"images": "iso_terminal_e.png",
    "label": "Terminal",
    "borders": borders(0.80, 0.80),
    "action": "terminal"},

    {"images": "iso_terminal_n.png",
    "label": "Terminal",
    "borders": borders(0.80, 0.80),
    "action": "terminal"},

    {"images": "iso_terminal_w.png",
    "label": "Terminal",
    "borders": borders(0.80, 0.80),
    "action": "terminal"},

    {"images": "iso_pillar_high.png",
    "borders": borders(-0.50, 0.25, -0.50, 0.25)},

    {"images": "iso_pillar_short.png",
    "borders": borders(-0.50, 0.25, -0.50, 0.25)},

    {"images": "iso_computerpillar_e.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_barrel.png",
    "label": "Barrel",
    "borders": borders(0.70, 0.70),
    "action": "barrel"},

    {"images": "iso_barrel_rusty.png",
    "label": "Barrel",
    "borders": borders(0.70, 0.70),
    "action": "barrel"},

    {"images": "iso_crate_ns.png",
    "label": "Crate",
    "borders": borders(0.80, 0.95),
    "action": "barrel"},

    {"images": "iso_crate_we.png",
    "label": "Crate",
    "borders": borders(0.80, 0.75),
    "action": "barrel"},

    {"images": "iso_lamp_s.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_raylamp_right.png",
    "borders": borders(-0.60, 0.55, -0.60, 0.50)},
    
    {"images": "iso_raylamp_down.png",
    "borders": borders(-0.60, 0.55, -0.60, 0.55)},

    {"images": "iso_raylamp_left.png",
    "borders": borders(-0.60, 0.50, -0.60, 0.55)},

    {"images": "iso_raylamp_up.png",
    "borders": borders(-0.60, 0.50, -0.60, 0.50)},

    {"images": "iso_fence_white_ns.png",
    "borders": borders(1.10, 2.20)},

    {"images": "iso_fence_white_we.png",
    "borders": borders(2.20, 1.10)},

    {"images": "iso_trapdoor_closed_n.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_trapdoor_closed_w.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_fence_wire_red_ns.png",
    "borders": borders(0.80, 2.20)},

    {"images": "iso_fence_wire_red_we.png",
    "borders": borders(2.20, 0.80)},

    {"images": "iso_fence_wire_green_ns.png",
    "borders": borders(0.80, 2.20)},

    {"images": "iso_fence_wire_green_we.png",
    "borders": borders(2.20, 0.80)},

    {"images": "iso_urinal_w.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_urinal_s.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_toilet_white_s.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_toilet_white_e.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_toilet_beige_w.png",
    "borders": borders(0.68, 0.50)},

    {"images": "iso_toilet_beige_n.png",
    "borders": borders(0.50, 0.68)},

    {"images": "iso_toilet_beige_e.png",
    "borders": borders(0.68, 0.50)},

    {"images": "iso_toilet_beige_s.png",
    "borders": borders(0.50, 0.68)},

    {"images": "iso_chair_brown_w.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_chair_brown_n.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_chair_brown_e.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_chair_brown_s.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_workdesk_w.png",
    "borders": borders(0.40, 1.00)},

    {"images": "iso_workdesk_n.png",
    "borders": borders(1.00, 0.40)},

    {"images": "iso_workdesk_e.png",
    "borders": borders(0.40, 1.00)},

    {"images": "iso_workdesk_s.png",
    "borders": borders(1.00, 0.40)},
    
    {"images": "iso_chair_white_w.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_chair_white_n.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_chair_white_s.png",
    "borders": borders(0.40, 0.40)},
    
    {"images": "iso_chair_white_e.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_bed_white_w.png",
    "borders": borders(1.10, 0.70)},

    {"images": "iso_bed_white_n.png",
    "borders": borders(0.70, 1.10)},

    {"images": "iso_bed_white_e.png",
    "borders": borders(1.10, 0.70)},

    {"images": "iso_bed_white_s.png",
    "borders": borders(0.70, 1.10)},

    {"images": "iso_bookshelf_long_w.png",
    "borders": borders(0.60, 2.20)},

    {"images": "iso_bookshelf_long_s.png",
    "borders": borders(2.20, 0.60)},

    {"images": "iso_bookshelf_long_e.png",
    "borders": borders(0.60, 2.20)},

    {"images": "iso_bookshelf_long_n.png",
    "borders": borders(2.20, 0.60)},

    {"images": "iso_bookshelf_s.png",
    "borders": borders(1.10, 0.60)},

    {"images": "iso_bookshelf_e.png",
    "borders": borders(0.60, 1.10)},

    {"images": "iso_bookshelf_w.png",
    "borders": borders(0.60, 1.10)},

    {"images": "iso_bookshelf_n.png",
    "borders": borders(1.10, 0.60)},

    {"images": "iso_bench_white_w.png",
    "borders": borders(0.70, 1.30)},

    {"images": "iso_bench_white_s.png",
    "borders": borders(1.30, 0.70)},
    
    {"images": "iso_bench_white_n.png",
    "borders": borders(1.30, 0.70)},

    {"images": "iso_bench_white_e.png",
    "borders": borders(0.70, 1.30)},

    {"images": "iso_bathtub_w.png",
    "borders": borders(1.50, 1.00)},

    {"images": "iso_bathtub_n.png",
    "borders": borders(1.00, 1.50)},

    {"images": "iso_tub_ns.png",
    "borders": borders(0.40, 0.50)},

    {"images": "iso_tub_we.png",
    "borders": borders(0.50, 0.40)},

    {"images": "iso_curtain_ns.png"},

    {"images": "iso_curtain_we.png"},

    {"images": "iso_sofa_white_w.png",
    "borders": borders(0.50, 1.00)},

    {"images": "iso_sofa_white_s.png",
    "borders": borders(1.00, 0.50)},

    {"images": "iso_sofa_white_e.png",
    "borders": borders(0.50, 1.00)},

    {"images": "iso_sofa_white_n.png",
    "borders": borders(1.00, 0.50)},

    {"images": "iso_tree_1.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_tree_2.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_tree_3.png",
    "borders": borders(0.60, 0.80)},

    {"images": "iso_wall_purple_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_purple_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_purple_curve_ws.png",
    "borders": borders(-0.55, 0.20, -0.20, 0.55)},

    {"images": "iso_wall_purple_nw.png",
    "borders": borders(-0.55, 0.20, -0.55, 0.20)},

    {"images": "iso_wall_purple_es.png",
    "borders": borders(-0.20, 0.55, -0.20, 0.55)},

    {"images": "iso_wall_purple_ne.png",
    "borders": borders(-0.20, 0.55, -0.55, 0.20)},

    {"images": "iso_wall_purple_T_nwe.png",
    "borders": borders(-0.55, 0.55, -0.55, 0.20)},

    {"images": "iso_wall_purple_T_nws.png",
    "borders": borders(-0.20, 0.55, -0.55, 0.55)},

    {"images": "iso_wall_purple_T_wes.png",
    "borders": borders(-0.55, 0.55, -0.20, 0.55)},

    {"images": "iso_wall_purple_T_ess.png",
    "borders": borders(-0.55, 0.20, -0.55, 0.55)},

    {"images": "iso_wall_cave_end_w.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_cave_end_n.png",
    "borders": borders(1.00, 1.00)},
    
    {"images": "iso_wall_cave_end_e.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_cave_end_s.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_grey_window_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_grey_window_ew.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_grey_striation_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_grey_striation_ew.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_brick_we.png",
    "borders": borders(1.20, 0.80)},

    {"images": "iso_wall_brick_ns.png",
    "borders": borders(0.80, 1.20),
    "after_smashing": 228},

    {"images": "iso_wall_brick_end_w.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_brick_edge_ws.png",
    "borders": borders(-0.60, 0.30, -0.60, 0.60)},

    {"images": "iso_wall_brick_edge_ne.png",
    "borders": borders(-0.60, 0.65, -0.60, 0.30)},

    {"images": "iso_wall_brick_edge_es.png",
    "borders": borders(-0.30, 0.60, -0.30, 0.60)},

    {"images": "iso_wall_brick_edge_nw.png",
    "borders": borders(-0.60, 0.30, -0.60, 0.30)},

    {"images": "iso_blood_1.png"},

    {"images": "iso_blood_3_1.png"},

    {"images": "iso_blood_3_2.png"},

    {"images": "iso_blood_3_3.png"},

    {"images": "iso_blood_8.png"},

    {"images": "iso_blood_4.png"},

    {"images": "iso_blood_5.png"},

    {"images": "iso_blood_10.png"},

    {"images": "iso_trapdoor_s.png"},

    {"images": "iso_trapdoor_e.png"},

    {"images": "iso_shroom_white_1.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_rock_big.png",
    "borders": borders(1.50, 1.50)},

    {"images": "iso_rock_small.png"},

    {"images": "iso_rock_pillar.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_red_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_red_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_turqois_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_turqois_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_shop_counter_s.png",
    "borders": borders(3.50, 1.50)},

    {"images": "iso_shop_counter_w.png",
    "borders": borders(1.50, 3.50)},

    {"images": "iso_shelf_s.png",
    "borders": borders(2.20, 0.60)},

    {"images": "iso_shelf_e.png",
    "borders": borders(0.60, 2.20)},

    {"images": "iso_shelf_n.png",
    "borders": borders(2.20, 0.60)},

    {"images": "iso_shelf_w.png",
    "borders": borders(0.60, 2.20)},

    {"images": "iso_wall_yellow_ellipsis_we.png",
    "borders": borders(-0.55, 0.55, -0.05, 0.60)},

    {"images": "iso_wall_yellow_ellipsis_dots_pipes_we.png",
    "borders": borders(-0.55, 0.55, -0.05, 0.60)},

    {"images": "iso_wall_yellow_ellipsis_dots_we.png",
    "borders": borders(-0.55, 0.55, -0.05, 0.60)},

    {"images": "iso_walls_yellow_we.png",
    "borders": borders(-0.55, 0.55, -0.05, 0.60)},

    {"images": "iso_wall_yellow_dots_pipes_we.png",
    "borders": borders(-0.55, 0.55, -0.05, 0.60)},

    {"images": "iso_wall_yellow_dots_we.png",
    "borders": borders(-0.55, 0.55, -0.05, 0.60)},

    {"images": "iso_walls_yellow_ns.png",
    "borders": borders(-0.05, 0.60, -0.55, 0.55)},

    {"images": "iso_wall_yellow_dots_pipes_ns.png",
    "borders": borders(-0.05, 0.60, -0.55, 0.55)},

    {"images": "iso_wall_yellow_dots_ns.png",
    "borders": borders(-0.05, 0.60, -0.55, 0.55)},

    {"images": "iso_wall_yellow_ellipsis_ns.png",
    "borders": borders(-0.05, 0.60, -0.55, 0.55)},

    {"images": "iso_wall_yellow_ellipsis_dots_pipes_ns.png",
    "borders": borders(-0.05, 0.60, -0.55, 0.55)},

    {"images": "iso_wall_yellow_ellipsis_dots_ns.png",
    "borders": borders(-0.05, 0.60, -0.55, 0.55)},

    {"images": "iso_wall_yellow_curve_long_es.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_wall_yellow_curve_long_ne.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_wall_yellow_curve_long_nw.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_wall_yellow_curve_long_ws.png",
    "borders": borders(1.10, 1.10)},

    {"images": ["iso_gate_unlocked_closed_ns_1.png", "iso_gate_unlocked_opened_ns_2.png", "iso_gate_unlocked_opened_ns_3.png", "iso_gate_unlocked_opened_ns_4.png", "iso_gate_unlocked_opened_ns_5.png"],
    "animation": "door"},

    {"images": ["iso_gate_unlocked_closed_we_1.png", "iso_gate_unlocked_opened_we_2.png", "iso_gate_unlocked_opened_we_3.png", "iso_gate_unlocked_opened_we_4.png", "iso_gate_unlocked_opened_we_5.png"],
    "animation": "door"},

    {"images": "iso_gate_locked_ns.png",
    "borders": borders(-0.05, 0.60, -1.55, 0.55)},

    {"images": "iso_gate_locked_we.png",
    "borders": borders(-1.55, 0.55, -0.05, 0.60)},

    {"images": "iso_computerpillar_n.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_computerpillar_w.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_computerpillar_s.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_chairs_ball_s.png",
    "borders": borders(0.80, 0.80)},

    {"images": "iso_chairs_ball_w.png",
    "borders": borders(0.80, 0.80)},

    {"images": "iso_chairs_ball_n.png",
    "borders": borders(0.80, 0.80)},

    {"images": "iso_chairs_ball_e.png",
    "borders": borders(0.80, 0.80)},

    {"images": "iso_sofa_red_s.png",
    "borders": borders(1.60, 0.80)},

    {"images": "iso_sofa_red_w.png",
    "borders": borders(0.80, 1.60)},

    {"images": "iso_sofa_red_n.png",
    "borders": borders(1.60, 0.80)},

    {"images": "iso_sofa_red_e.png",
    "borders": borders(0.80, 1.60)},

    {"images": "iso_body_redguard_1.png"},

    {"images": "iso_body_redguard_2.png"},

    {"images": "iso_body_redguard_4.png"},

    {"images": "iso_body_redguard_3.png"},

    {"images": "iso_conference_table_nw.png",
    "borders": borders(2.00, 2.00)},

    {"images": "iso_conference_table_ne.png",
    "borders": borders(2.00, 2.00)},

    {"images": "iso_conference_table_es.png",
    "borders": borders(2.00, 2.00)},

    {"images": "iso_conference_table_ws.png",
    "borders": borders(2.00, 2.00)},

    {"images": "iso_wall_redbrownspiked_ns.png",
    "borders": borders(0.80, 2.30)},

    {"images": "iso_wall_redbrownspiked_we.png",
    "borders": borders(2.30, 0.80)},

    {"images": "iso_sleepingcapsule_n.png",
    "borders": borders(1.20, 2.00)},

    {"images": "iso_sleepingcapsule_w.png",
    "borders": borders(2.00, 1.20)},

    {"images": "iso_sleepingcapsule_s.png",
    "borders": borders(1.20, 2.00)},

    {"images": "iso_sleepingcapsule_e.png",
    "borders": borders(2.00, 1.20)},

    {"images": "iso_sleepingcapsule_double_n.png",
    "borders": borders(1.20, 2.00)},

    {"images": "iso_sleepingcapsule_double_e.png",
    "borders": borders(2.00, 1.20)},

    {"images": "iso_sleepingcapsule_double_s.png",
    "borders": borders(1.20, 2.00)},

    {"images": "iso_sleepingcapsule_double_w.png",
    "borders": borders(2.00, 1.20)},

    {"images": "iso_cinematograph_e.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_cinematograph_w.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_lamp_n.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_lamp_e.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_lamp_w.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_shroom_blue_1.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_shroom_blue_2.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_shroom_blue_3.png",
    "borders": borders(0.90, 0.90)},

    {"images": "iso_shroom_white_2.png",
    "borders": borders(0.90, 0.90)},

    {"images": "iso_wall_brick_T_nwe.png",
    "borders": borders(1.20, 1.20)},

    {"images": "iso_wall_brick_T_nes.png",
    "borders": borders(1.20, 1.20)},

    {"images": "iso_wall_brick_T_wes.png",
    "borders": borders(1.20, 1.20)},

    {"images": "iso_wall_brick_T_nws.png",
    "borders": borders(1.20, 1.20)},

    {"images": "iso_wall_brick_cracked_ns.png",
    "borders": borders(0.50, 1.20),
    "after_smashing": 221,
    "action": "barrel"},

    {"images": "iso_wall_brick_cracked_we.png",
    "borders": borders(1.20, 0.50),
    "after_smashing": 222,
    "action": "barrel"},

    {"images": "iso_wall_brick_smashed_ns.png"},

    {"images": "iso_wall_brick_smashed_we.png"},

    {"images": "iso_projectionscreen_s.png",
    "borders": borders(2.20, 1.00)},

    {"images": "iso_projectionscreen_w.png",
    "borders": borders(1.00, 2.20)},

    {"images": "iso_projectionscreen_n.png",
    "borders": borders(2.00, 1.00)},

    {"images": "iso_projectionscreen_e.png",
    "borders": borders(1.00, 2.20)},

    {"images": "iso_cinematograph_n.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_cinematograph_s.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_sign_questionmark.png",
    "label": "Sign",
    "borders": borders(0.50, 0.60),
    "action": "sign"},

    {"images": "iso_sign_exclamationmark.png",
    "label": "Sign",
    "borders": borders(0.60, 0.50),
    "action": "sign"},

    {"images": "iso_sign_lessthenmark.png",
    "label": "Sign",
    "borders": borders(0.50, 0.60),
    "action": "sign"},

    {"images": "iso_wall_green_wallpaper_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_green_wallpaper_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_green_brown_manyspots_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_green_brown_manyspots_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_green_brown_fewspots_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_green_brown_fewspots_ew.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_counter_small_w.png",
    "borders": borders(0.80, 1.05)},

    {"images": "iso_counter_small_n.png",
    "borders": borders(1.05, 0.80)},

    {"images": "iso_counter_small_e.png",
    "borders": borders(0.80, 1.05)},

    {"images": "iso_counter_small_s.png",
    "borders": borders(1.05, 0.80)},

    {"images": "iso_counter_small_curve_nw.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_counter_small_curve_ne.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_counter_small_curve_es.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_counter_small_curve_ws.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_counter_small_edge_ws.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_counter_small_edge_nw.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_counter_small_edge_ne.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_counter_small_edge_es.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_library_counter_we.png",
    "borders": borders(3.50, 1.50)},

    {"images": "iso_library_counter_ns.png",
    "borders": borders(1.50, 3.50)},

    {"images": "iso_bathtub_e.png",
    "borders": borders(1.50, 1.00)},

    {"images": "iso_bathtub_s.png",
    "borders": borders(1.00, 1.50)},

    {"images": "iso_table_round_yellow.png",
    "borders": borders(0.80, 0.80)},

    {"images": "iso_ladderring_n.png"},

    {"images": "iso_ladderring_w.png"},

    {"images": "iso_wall_yellow_curve_short_es.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_yellow_curve_short_ne.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_yellow_curve_short_nw.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_yellow_curve_short_ws.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_table_elliptic_yellow_ns.png",
    "borders": borders(0.85, 1.50)},

    {"images": "iso_table_elliptic_yellow_ew.png",
    "borders": borders(1.50, 0.85)},

    {"images": "iso_table_glass_ns.png",
    "borders": borders(1.00, 1.20)},

    {"images": "iso_table_glass_we.png",
    "borders": borders(1.20, 1.00)},

    {"images": "iso_wall_glass_ns.png",
    "borders": borders(0.40, 1.10),
    "after_smashing": 332,
    "action": "barrel",
    "smashed_sound": "Glass_Break.ogg"},

    {"images": "iso_wall_glass_we.png",
    "borders": borders(1.10, 0.40),
    "after_smashing": 430,
    "action": "barrel",
    "smashed_sound": "Glass_Break.ogg"},

    {"images": "iso_wall_turquois_window_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_turquois_window_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_red_window_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_red_window_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_green_wallpaper_window_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_green_wallpaper_window_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_wall_green_brown_manyspots_window_ns.png",
    "borders": borders(0.40, 1.10)},

    {"images": "iso_wall_green_brown_manyspots_window_we.png",
    "borders": borders(1.10, 0.40)},

    {"images": "iso_barshelf_middle_we.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_middle_ns.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_left_ns.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_left_we.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_right_we.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_left_ew.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_rightouter_ew.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_rightouter_we.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_rightouter_ns.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_barshelf_leftouter_we.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_bench_red_w.png",
    "borders": borders(0.60, 1.20)},

    {"images": "iso_bench_red_n.png",
    "borders": borders(1.20, 0.60)},

    {"images": "iso_bench_red_e.png",
    "borders": borders(0.60, 1.20)},

    {"images": "iso_bench_red_s.png",
    "borders": borders(1.20, 0.60)},

    {"images": "iso_stool_brown_w.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_stool_brown_n.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_stool_brown_e.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_stool_brown_s.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_stool_plant_brown_w.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_stool_plant_brown_n.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_stool_plant_brown_e.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_stool_plant_brown_s.png",
    "borders": borders(0.60, 0.60)},

    {"images": "iso_oil_1.png"},

    {"images": "iso_oil_5_1.png"},

    {"images": "iso_oil_4_1.png"},

    {"images": "iso_oil_4_2.png"},

    {"images": "iso_oil_10.png"},

    {"images": "iso_oil_7.png"},

    {"images": "iso_oil_5_2.png"},

    {"images": "iso_oil_11.png"},

    {"images": "iso_pathblocker_1x1.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_wall_brick_longend_we.png",
    "borders": borders(1.20, 0.80),
    "after_smashing": 235},

    {"images": "iso_wall_brick_longend_ns.png",
    "borders": borders(0.80, 1.20),
    "after_smashing": 236},

    {"images": "iso_autogun_w.png",
    "borders": borders(0.70, 0.70)},

    {"images": "iso_autogun_n.png",
    "borders": borders(0.70, 0.70)},

    {"images": "iso_autogun_e.png",
    "borders": borders(0.70, 0.70)},

    {"images": "iso_autogun_s.png",
    "borders": borders(0.70, 0.70)},

    {"images": "iso_wall_brick_cable_we.png",
    "borders": borders(1.20, 0.80)},

    {"images": "iso_wall_brick_cable_ns.png",
    "borders": borders(0.80, 1.20)},

    {"images": "iso_wall_brick_cable_edge_ws.png",
    "borders": borders(-0.60, 0.30, -0.60, 0.60)},

    {"images": "iso_wall_brick_cable_edge_ne.png",
    "borders": borders(-0.60, 0.65, -0.60, 0.30)},

    {"images": "iso_wall_brick_cable_edge_es.png",
    "borders": borders(-0.30, 0.60, -0.30, 0.60)},

    {"images": "iso_wall_brick_cable_edge_nw.png",
    "borders": borders(-0.60, 0.30, -0.60, 0.30)},

    {"images": "iso_restaurant_counter_w.png",
    "borders": borders(1.50, 5.00)},

    {"images": "iso_restaurant_counter_n.png",
    "borders": borders(5.00, 1.50)},

    {"images": "iso_bar_counter_w.png",
    "borders": borders(0.65, 5.50)},

    {"images": "iso_bar_counter_s.png",
    "borders": borders(5.50, 0.65)},

    {"images": "iso_crystal_pillar_1.png",
    "borders": borders(0.50, 0.50)},

    {"images": "iso_crystal_pillar_2.png",
    "borders": borders(1.15, 1.15)},

    {"images": "iso_crystal_stump_1.png",
    "borders": borders(0.95, 0.95)},

    {"images": "iso_crystal_stump_2.png",
    "borders": borders(1.25, 1.05)},

    {"images": "iso_crystal_pillar_3.png",
    "borders": borders(1.20, 1.05)},

    {"images": "iso_crystal_stump_3.png",
    "borders": borders(1.10, 1.10)},

    {"images": "iso_wall_corners_es.png",
    "borders": borders(1.10, 1.00)},

    {"images": "iso_wall_corners_ws.png",
    "borders": borders(1.10, 1.00)},
    
    {"images": "iso_wall_corners_nw.png",
    "borders": borders(1.10, 1.00)},

    {"images": "iso_wall_corners_ne.png",
    "borders": borders(1.10, 1.00)},

    {"images": "iso_wall_glass_broken_ns.png"},

    {"images": "iso_gate_unlocked_opened_ns_5_blocked.png"},

    {"images": "iso_gate_unlocked_opened_we_5_blocked.png"},

    {"images": "iso_doubledoor_locked_we.png",
    "borders": borders(-0.55, 1.55, -0.80, 0.20)},

    {"images": "iso_doubledoor_locked_ns.png",
    "borders": borders(-0.80, 0.20, -0.55, 1.55)},

    {"images": ["iso_doubledoor_unlocked_opened_we_1.png", "iso_doubledoor_unlocked_opened_we_2.png", "iso_doubledoor_unlocked_opened_we_3.png", "iso_doubledoor_unlocked_opened_we_4.png", "iso_doubledoor_unlocked_opened_we_5.png"],
    "animation": "door"},

    {"images": ["iso_doubledoor_unlocked_opened_ns_1.png", "iso_doubledoor_unlocked_opened_ns_2.png", "iso_doubledoor_unlocked_opened_ns_3.png", "iso_doubledoor_unlocked_opened_ns_4.png", "iso_doubledoor_unlocked_opened_ns_5.png"],
    "animation": "door"},

    {"images": "iso_basin_n.png",
    "borders": borders(1.05, 0.95)},

    {"images": "iso_basin_e.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_basin_s.png",
    "borders": borders(1.05, 0.95)},

    {"images": "iso_basin_w.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_deskchair_w.png",
    "borders": borders(0.90, 0.90)},

    {"images": "iso_deskchair_n.png",
    "borders": borders(0.90, 0.90)},

    {"images": "iso_deskchair_e.png",
    "borders": borders(0.90, 0.90)},

    {"images": "iso_ladder_w.png"},

    {"images": "iso_ladder_n.png"},

    {"images": "iso_chest_greyrusty_closed_w.png",
    "label": "Chest",
    "borders": borders(0.60, 0.80),
    "action": "chest",
    "after_looting": 350},

    {"images": "iso_chest_greyrusty_closed_n.png",
    "label": "Chest",
    "borders": borders(0.80, 0.60),
    "action": "chest",
    "after_looting": 351},

    {"images": "iso_chest_greyrusty_opened_w.png",
    "borders": borders(0.60, 0.80)},

    {"images": "iso_chest_greyrusty_opened_n.png",
    "borders": borders(0.80, 0.60)},

    {"images": "iso_chest_greyrusty_closed_s.png",
    "label": "Chest",
    "borders": borders(0.80, 0.60),
    "action": "chest",
    "after_looting": 354},

    {"images": "iso_chest_greyrusty_closed_e.png",
    "label": "Chest",
    "borders": borders(0.60, 0.80),
    "action": "chest",
    "after_looting": 355},

    {"images": "iso_chest_greyrusty_opened_s.png",
    "borders": borders(0.80, 0.60)},

    {"images": "iso_chest_greyrusty_opened_e.png",
    "borders": borders(0.60, 0.80)},

    {"images": "iso_security_gate_opened_w.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_security_gate_opened_n.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_security_gate_closed_w.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_security_gate_closed_n.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_security_gate_opened_e.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_security_gate_opened_s.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_security_gate_closed_e.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_security_gate_closed_s.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_solarpanel.png",
    "label": "Solar Panel",
    "borders": borders(0.95, 1.05),
    "after_smashing": 407,
    "action": "barrel"},

    {"images": "iso_conveyor_ns.png",
    "borders": borders(3.00, 2.00)},

    {"images": "iso_conveyor_we.png",
    "borders": borders(2.00, 3.00)},

    {"images": "iso_ramp_w.png",
    "borders": borders(2.46, 1.94)},

    {"images": "iso_ramp_s.png",
    "borders": borders(1.94, 2.46)},

    {"images": "iso_ramp_e.png",
    "borders": borders(2.46, 1.94)},

    {"images": "iso_ramp_n.png",
    "borders": borders(1.94, 2.46)},

    {"images": "iso_tesla_n.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_tesla_w.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_tesla_s.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_tesla_e.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_roboarm_1_n.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_roboarm_1_w.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_freighter_railway_ns.png",
    "borders": borders(3.00, 3.00)},

    {"images": "iso_freighter_railway_we.png",
    "borders": borders(3.00, 3.00)},

    {"images": "iso_freighter_railway_end_s.png",
    "borders": borders(3.00, 3.00)},

    {"images": "iso_freighter_railway_end_e.png",
    "borders": borders(3.00, 3.00)},

    {"images": "iso_freighter_railway_end_n.png",
    "borders": borders(3.00, 3.00)},

    {"images": "iso_freighter_railway_end_w.png",
    "borders": borders(3.00, 3.00)},

    {"images": "iso_solarpanel_pillar.png",
    "borders": borders(0.95, 1.05)},

    {"images": "iso_crate_ns_megasys.png",
    "label": "Crate",
    "borders": borders(0.80, 0.95),
    "action": "barrel"},

    {"images": "iso_reactor_w.png",
    "borders": borders(4.50, 4.00)},

    {"images": "iso_reactor_s.png",
    "borders": borders(4.00, 4.50)},

    {"images": "iso_reactor_e.png",
    "borders": borders(4.50, 4.00)},

    {"images": "iso_reactor_n.png",
    "borders": borders(4.00, 4.50)},

    {"images": "iso_wallterminal_n.png",
    "label": "Terminal",
    "borders": borders(0.60, 0.40),
    "action": "terminal"},

    {"images": "iso_wallterminal_w.png",
    "label": "Terminal",
    "borders": borders(0.40, 0.60),
    "action": "terminal"},

    {"images": "iso_wallterminal_s.png",
    "label": "Terminal",
    "borders": borders(0.60, 0.40),
    "action": "terminal"},

    {"images": "iso_wallterminal_e.png",
    "label": "Terminal",
    "borders": borders(0.40, 0.60),
    "action": "terminal"},

    {"images": "iso_turbines_n.png",
    "borders": borders(1.10, 1.80)},

    {"images": "iso_turbines_w.png",
    "borders": borders(1.80, 1.05)},

    {"images": "iso_turbines_s.png",
    "borders": borders(1.10, 1.80)},

    {"images": "iso_turbines_e.png",
    "borders": borders(1.80, 1.05)},

    {"images": "iso_weapon_crate.png",
    "label": "Weapon Crate",
    "borders": borders(1.30, 1.30),
    "action": "barrel"},

    {"images": "iso_electronicscrap_1.png"},

    {"images": "iso_electronicscrap_2.png"},

    {"images": "iso_electronicscrap_3.png"},

    {"images": "iso_electronicscrap_4.png"},

    {"images": "iso_electronicscrap_5.png"},

    {"images": "iso_electronicscrap_6.png"},

    {"images": "iso_electronicscrap_7.png"},

    {"images": "iso_electronicscrap_8.png"},

    {"images": "iso_body_human.png"},

    {"images": "iso_ladder_short_n.png"},

    {"images": "iso_ladder_short_w.png"},

    {"images": "iso_wrecked_car_w.png",
    "borders": borders(1.40, 2.80)},

    {"images": "iso_wrecked_car_s.png",
    "borders": borders(2.80, 1.40)},

    {"images": "iso_wrecked_car_e.png",
    "borders": borders(1.40, 2.80)},

    {"images": "iso_wrecked_car_n.png",
    "borders": borders(2.80, 1.40)},
    
    {"images": "iso_toilet_white_n.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_toilet_white_w.png",
    "borders": borders(0.40, 0.40)},

    {"images": "iso_roboarm_1_s.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_roboarm_1_e.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_roboarm_2_n.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_roboarm_2_w.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_roboarm_2_s.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_roboarm_2_e.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_crushed_476.png",
    "borders": borders(2.10, 2.60)},

    {"images": "iso_wall_glass_broken_we.png"},

    {"images": ["iso_sign_questionmark_anim_dark.png", "iso_sign_questionmark_anim_bright.png"],
    "label": "Sign",
    "borders": borders(0.50, 0.60),
    "action": "sign",
    "fps": 0.44},

    {"images": ["iso_sign_exclamationmark_anim_dark.png", "iso_sign_exclamationmark_anim_bright.png"],
    "label": "Sign",
    "borders": borders(0.60, 0.50),
    "action": "sign",
    "fps": 0.4},

    {"images": ["iso_sign_lessthenmark_anim_dark.png", "iso_sign_lessthenmark_anim_bright.png"],
    "label": "Sign",
    "borders": borders(0.50, 0.60),
    "action": "sign",
    "fps": 0.6},

    {"images": ["iso_barrel_radioactive.png"],
    "borders": borders(0.70, 0.70)},

    {"images": "iso_vendingmachine_blue_w.png",
    "label": "Vending Machine",
    "borders": borders(1.10, 1.55),
    "action": "shop"},

    {"images": "iso_vendingmachine_blue_s.png",
    "label": "Vending Machine",
    "borders": borders(1.55, 1.10),
    "action": "shop"},

    {"images": "iso_vendingmachine_blue_e.png",
    "label": "Vending Machine",
    "borders": borders(1.10, 1.55),
    "action": "shop"},

    {"images": "iso_vendingmachine_blue_n.png",
    "label": "Vending Machine",
    "borders": borders(1.55, 1.10),
    "action": "shop"},

    {"images": "iso_vendingmachine_white_w.png",
    "label": "Vending Machine",
    "borders": borders(1.00, 1.55),
    "action": "shop"},

    {"images": "iso_vendingmachine_white_s.png",
    "label": "Vending Machine",
    "borders": borders(1.55, 1.00),
    "action": "shop"},

    {"images": "iso_vendingmachine_white_e.png",
    "label": "Vending Machine",
    "borders": borders(1.00, 1.55),
    "action": "shop"},

    {"images": "iso_vendingmachine_white_n.png",
    "label": "Vending Machine",
    "borders": borders(1.55, 1.00),
    "action": "shop"},

    {"images": "iso_vendingmachine_red_w.png",
    "label": "Vending Machine",
    "borders": borders(1.10, 1.55),
    "action": "shop"},

    {"images": "iso_vendingmachine_red_s.png",
    "label": "Vending Machine",
    "borders": borders(1.55, 1.10),
    "action": "shop"},

    {"images": "iso_vendingmachine_red_e.png",
    "label": "Vending Machine",
    "borders": borders(1.10, 1.55),
    "action": "shop"},

    {"images": "iso_vendingmachine_red_n.png",
    "label": "Vending Machine",
    "borders": borders(1.55, 1.10),
    "action": "shop"},

    {"images": "iso_transformer.png",
    "borders": borders(0.95, 0.95)},

    {"images": "iso_transformer_rusty.png",
    "borders": borders(0.95, 0.95)},

    {"images": "iso_transformer_sparkles.png",
    "borders": borders(0.95, 0.95)},

    {"images": "iso_bookshelf_lootable_e.png",
    "borders": borders(0.60, 1.10),
    "action": "chest",
    "label": "Bookshelf",
    "after_looting": 443},

    {"images": "iso_bookshelf_looted_e.png",
    "borders": borders(0.60, 1.10)},

    {"images": "iso_bookshelf_lootable_s.png",
    "borders": borders(1.10, 0.60),
    "action": "chest",
    "label": "Bookshelf",
    "after_looting": 441},

    {"images": "iso_bookshelf_looted_s.png",
    "borders": borders(1.10, 0.60)},

    {"images": "iso_bookshelf_lootable_w.png",
    "borders": borders(0.60, 1.10),
    "action": "chest",
    "label": "Bookshelf",
    "after_looting": 447},

    {"images": "iso_bookshelf_looted_w.png",
    "borders": borders(0.60, 1.10)},

    {"images": "iso_bookshelf_lootable_n.png",
    "borders": borders(1.10, 0.60),
    "action": "chest",
    "label": "Bookshelf",
    "after_looting": 449},

    {"images": "iso_bookshelf_looted_n.png",
    "borders": borders(1.10, 0.60)},

    {"images": "iso_bookshelf_long_lootable_e.png",
    "borders": borders(0.60, 2.20),
    "action": "chest",
    "label": "Bookshelf",
    "after_looting": 451},

    {"images": "iso_bookshelf_long_looted_e.png",
    "borders": borders(0.60, 2.20)},

    {"images": "iso_bookshelf_long_lootable_s.png",
    "borders": borders(2.20, 0.60),
    "action": "chest",
    "label": "Bookshelf",
    "after_looting": 453},

    {"images": "iso_bookshelf_long_looted_s.png",
    "borders": borders(2.20, 0.60)},

    {"images": "iso_bookshelf_long_lootable_w.png",
    "borders": borders(0.60, 2.20),
    "action": "chest",
    "label": "Bookshelf",
    "after_looting": 455},

    {"images": "iso_bookshelf_long_looted_w.png",
    "borders": borders(0.60, 2.20)},

    {"images": "iso_bookshelf_long_lootable_n.png",
    "borders": borders(2.20, 0.60),
    "action": "chest",
    "label": "Bookshelf",
    "after_looting": 457},

    {"images": "iso_bookshelf_long_looted_n.png",
    "borders": borders(2.20, 0.60)},

    {"images": "iso_trapdoor_closed_e.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_trapdoor_closed_s.png",
    "borders": borders(1.00, 1.00)},

    {"images": "iso_statue_883_e.png",
    "borders": borders(1.80, 1.80),
    "after_smashing": 464,
    "action": "barrel",
    "label": "Statue"},

    {"images": "iso_statue_883_n.png",
    "borders": borders(1.80, 1.80),
    "after_smashing": 465,
    "action": "barrel",
    "label": "Statue"},

    {"images": "iso_statue_883_s.png",
    "borders": borders(1.80, 1.80),
    "after_smashing": 466,
    "action": "barrel",
    "label": "Statue"},

    {"images": "iso_statue_883_w.png",
    "borders": borders(1.80, 1.80),
    "after_smashing": 467,
    "action": "barrel",
    "label": "Statue"},

    {"images": "iso_statue_883_smashed_e.png",
    "borders": borders(1.80, 1.80)},

    {"images": "iso_statue_883_smashed_n.png",
    "borders": borders(1.80, 1.80)},

    {"images": "iso_statue_883_smashed_s.png",
    "borders": borders(1.80, 1.80)},

    {"images": "iso_statue_883_smashed_w.png",
    "borders": borders(1.80, 1.80)},

    {"images": { "iso_terminal_secure_e_01.png", "iso_terminal_secure_e_02.png", "iso_terminal_secure_e_03.png", "iso_terminal_secure_e_04.png", "iso_terminal_secure_e_05.png", "iso_terminal_secure_e_06.png", "iso_terminal_secure_e_07.png", "iso_terminal_secure_e_08.png", "iso_terminal_secure_e_09.png", "iso_terminal_secure_e_10.png", "iso_terminal_secure_e_11.png", "iso_terminal_secure_e_12.png", "iso_terminal_secure_e_13.png" },
    "label": "Secure terminal",
    "borders": borders(0.80, 0.80),
    "action": "terminal",
    "fps": 12},

    {"images": ["iso_terminal_secure_s_01.png", "iso_terminal_secure_s_02.png", "iso_terminal_secure_s_03.png", "iso_terminal_secure_s_04.png", "iso_terminal_secure_s_05.png", "iso_terminal_secure_s_06.png", "iso_terminal_secure_s_07.png", "iso_terminal_secure_s_08.png", "iso_terminal_secure_s_09.png", "iso_terminal_secure_s_10.png", "iso_terminal_secure_s_11.png", "iso_terminal_secure_s_12.png", "iso_terminal_secure_s_13.png"],
    "label": "Secure terminal",
    "borders": borders(0.80, 0.80),
    "action": "terminal",
    "fps": 12},

    {"images": "iso_terminal_secure_w_01.png",
    "label": "Secure terminal",
    "borders": borders(0.80, 0.80),
    "action": "terminal"},

    {"images": "iso_terminal_secure_n_01.png",
    "label": "Secure terminal",
    "borders": borders(0.80, 0.80),
    "action": "terminal",
    "fps": 12}
]
