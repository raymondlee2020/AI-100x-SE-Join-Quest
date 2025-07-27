def before_scenario(context, scenario):
    # Reset game state before each scenario
    context.game = None
    context.move_result = None
    context.move_error = None
    context.from_pos = None
    context.to_pos = None