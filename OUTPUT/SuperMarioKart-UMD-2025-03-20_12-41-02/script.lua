--data.prev_y_pos = 2288 --this is where mario starts 
data.prev_checkpoint = 29 --this is where mario starts
data.r = 0

function speedReward()
    -- Give a reward if the speed is non zero (aka the cart is moving)
    local reward = 0

    if (data.isTurnedAround ~= 0) or (data.isTurnedAround == 16) then
        reward = -20
    elseif data.kart1_speed > 500 then
        reward = 5
    elseif data.kart1_speed > 0 then
        reward = 0.1
    elseif data.kart1_speed == 0 then
        reward = -25
    end
    return reward
   
end

function roadReward()
    -- Give a penalty if not on road.
    local reward = 0

    if data.surface ~= 64 then
        reward = -15
    elseif data.surface == 64 then
        reward = 20
    end
    return reward
end


function checkpointReward()
    -- Give a reward if the checkpoint is increasing, penalize if decreasing.
    local reward = 0
    if (data.current_checkpoint ~= data.prev_checkpoint) then
        --print("Prev checkpoint: " .. data.prev_checkpoint .. ", Current checkpoint: " .. data.current_checkpoint)
    end

    if (data.current_checkpoint == data.prev_checkpoint + 1) then
        reward = 50
    elseif (data.prev_checkpoint == 29) and (data.current_checkpoint == 0) then
        reward = 50
    elseif (data.current_checkpoint == data.prev_checkpoint - 1) then
        reward = -100
    end
    data.prev_checkpoint = data.current_checkpoint


    return reward
end

function timeReward()
    local timeReward = 0

    if data.current_checkpoint == 4 then
        if data.currSec < 6 then
            timeReward = 500
        elseif data.currSec < 7 then
            timeReward = 400
        elseif data.currSec < 8 then
            timeReward = 300
        elseif data.currSec < 9 then
            timeReward = 200
        elseif data.currSec < 10 then
            timeReward = 100
        else
            timeReward = 0
        end
    else
        timeReward = 0
    end
    return timeReward
end


function getReward()
    local total_reward = checkpointReward() + speedReward() + roadReward() + timeReward()
    --print("Reward" .. total_reward)
    data.r = data.r + total_reward
    return total_reward --checkpointReward() + speedReward() + roadReward()
    
end

function isDone()
    -- The scenario ends when the current checkpoint is greater than 3 and the kart is moving
    --print(data.currSec)
    if (data.current_checkpoint == 4) then--and (data.kart1_speed > 0) then--(data.prev_checkpoint == 2) then
        print('I made it to the checkpoint.')
        if (data.kart1_speed > 0) then
            print('I am done. Training reward: ' .. data.r)
            return true
        end
    elseif (data.currSec > 15) and (data.currSec < 150) then -- prevents the weird bogus 5555 I'm getting
        print('I have timed out at checkpoint:' .. data.current_checkpoint)
        return true
    end
    
    return false
end
