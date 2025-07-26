-- Global Variables
checkpoints = {
    {x = 3712, y = 2255},  
    {x = 3690, y = 1853},
    {x = 3502, y = 1536},
    {x = 3256, y = 1422},
    {x = 2870, y = 1228},
    {x = 2554, y = 1080},
    {x = 2279, y = 944}
}

-- State Tracking Variables
initial_x_pos = 3712
initial_y_pos = 2288

next_checkpoint = 1
checkpoint_x = checkpoints[next_checkpoint].x
checkpoint_y = checkpoints[next_checkpoint].y

dist_to_checkpoint = math.sqrt((initial_x_pos - checkpoint_x)^2 + (initial_y_pos - checkpoint_y)^2)
prev_dist_to_checkpoint = dist_to_checkpoint

total_reward = 0
end_condition = false
passed_checkpoints = {}

function distanceToNextCheckpoint()
    if type(data) == "table" and data.kart1_X and data.kart1_Y then
        local dx = data.kart1_X - checkpoint_x
        local dy = data.kart1_Y - checkpoint_y
        return math.sqrt(dx*dx + dy*dy)
    else
        return prev_dist_to_checkpoint or 0
    end
end

function checkpointDistanceReward()
    local reward = 0

    if type(data) ~= "table" or not data.kart1_X or not data.kart1_Y then
        print("[Lua] ⚠️ Data not ready. Skipping reward calculation.")
        return 0
    end

    local current_dist = distanceToNextCheckpoint()
    local progress = prev_dist_to_checkpoint - current_dist

    -- Reward for getting closer
    if progress > 0 then
        reward = reward + progress * 0.01
        prev_dist_to_checkpoint = current_dist
    end

    -- Check if checkpoint reached
    local reach_radius = 5.0
    if data.current_checkpoint == next_checkpoint and not passed_checkpoints[next_checkpoint] then
        reward = reward + 1.0
        passed_checkpoints[next_checkpoint] = true

        if next_checkpoint < #checkpoints then
            next_checkpoint = next_checkpoint + 1
            checkpoint_x = checkpoints[next_checkpoint].x
            checkpoint_y = checkpoints[next_checkpoint].y
            prev_dist_to_checkpoint = distanceToNextCheckpoint()
            print("[Lua] 🚩 Next checkpoint:", next_checkpoint)
        else
            print("[Lua] ✅ Final checkpoint reached.")
            end_condition = true
        end
    end

    return reward
end

-- Top-Level API Functions
function getReward()
    local step_reward = checkpointDistanceReward()

    if end_condition then
        step_reward = step_reward + 100
    end

    total_reward = total_reward + step_reward
    return step_reward
end

function isDone()
    return end_condition
end
