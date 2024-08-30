#version 450 core   

out vec4 FragColor;


uniform vec2 iResolution; 
uniform float iTime;

uniform int lights_on;
uniform int view_all;
uniform vec2 player;
uniform vec2 mouse;

uniform float ray_dist;

uniform vec2 grid_size;
uniform int map[25 * 25];


const float circle_size = 0.01;


// FUNCTION TO DRAW LINES IF NEEDED
float line(vec2 p1, vec2 p2, vec2 p3, float thickness) {
    vec2 p12 = p2 - p1;
    vec2 p13 = p3 - p1;

    float d = dot(p12, p13) / length(p12);
    
    vec2 p4 = p1 + normalize(p12) * d;

    if (length(p4 - p3) < thickness && 
        length(p4 - p1) < length(p12) && 
        length(p4 - p2) < length(p12)) {
        return 1.0;
    } else {
        return 0.0;
    }
}


// FUNCTION TO GET THE DIRECTION BETWEEN 2 LINES
vec2 get_direction(vec2 start, vec2 end) {
    vec2 vector = normalize(end - start);
    return vector; 
} 


// FUNCTION TO RAY TRACE A LINE
vec3 ray_trace(vec2 start, vec2 end, float max_dist) {
    vec2 direction = get_direction(start, end);

    float step_x;
    if (direction.x != 0.0) {
        step_x = sqrt(1 + (direction.y / direction.x) * (direction.y / direction.x));
    } else { step_x = 1.0e9; }

    float step_y;
    if (direction.y != 0) {
        step_y = sqrt(1 + (direction.x / direction.y) * (direction.x / direction.y));
    } else { step_y = 1.0e9; }
    vec2 vRayUnitStepSize = vec2(step_x, step_y);


    vec2 vMapCheck = floor(start);
    vec2 vRayLength1D = vec2(0.0, 0.0);
    vec2 vStep = vec2(0.0, 0.0);

    if (direction.x < 0.0) {
        vStep.x = -1.0;
        vRayLength1D.x = (start.x - float(vMapCheck.x)) * vRayUnitStepSize.x;
    } else {
        vStep.x = 1.0;
        vRayLength1D.x = (float(vMapCheck.x + 1.0) - start.x) * vRayUnitStepSize.x;
    }

    if (direction.y < 0.0) {
        vStep.y = -1.0;
        vRayLength1D.y = (start.y - float(vMapCheck.y)) * vRayUnitStepSize.y;
    } else {
        vStep.y = 1.0;
        vRayLength1D.y = (float(vMapCheck.y + 1.0) - start.y) * vRayUnitStepSize.y;
    }


    bool bTileFound = false;
    float fDistance = 0.0;
    float fMaxDistance = max_dist;
    for (float iters=0.0; !bTileFound && (fDistance < fMaxDistance); iters++) {

        if (vRayLength1D.x < vRayLength1D.y) {
            vMapCheck.x += vStep.x;
            fDistance = vRayLength1D.x;

            if ((vRayLength1D.x + vRayUnitStepSize.x) < fMaxDistance) {
                vRayLength1D.x += vRayUnitStepSize.x;
            } else {
                vRayLength1D.x = fMaxDistance;
            }

        } else {
            vMapCheck.y += vStep.y;
            fDistance = vRayLength1D.y;

            if ((vRayLength1D.y + vRayUnitStepSize.y) < fMaxDistance) {
                vRayLength1D.y += vRayUnitStepSize.y;
            } else {
                vRayLength1D.y = fMaxDistance;;
            }
        }

        if (vMapCheck.x >= 0.0 && vMapCheck.x < grid_size.x && vMapCheck.y >= 0.0 && vMapCheck.y < grid_size.y) {
            if (map[int(grid_size.x * vMapCheck.x + vMapCheck.y)] == 1.0) {
                bTileFound = true;
                break;
            }
        } else {
            break;
        }
    }

    vec2 collision = start + direction * fDistance;

    if (length(collision - start) > length(end - start)) {
        
        if (bTileFound) {
            return vec3(1.0, vMapCheck);
        } else {
            return vec3(1.0, vec2(-2.0));
        }
    } else {
        return vec3(0.0, vec2(-2.0));
    }
}



void main() {

    //INIT MAIN VARIABLES
    vec2 invertedCoord = vec2(gl_FragCoord.x, iResolution.y - gl_FragCoord.y);

    vec2 player_uv = player / iResolution;
    vec2 mouse_uv = mouse / iResolution;
    vec2 uv = invertedCoord / iResolution;

    vec2 player_grid_uv = player_uv * grid_size;
    vec2 mouse_grid_uv = mouse_uv * grid_size;
    vec2 grid_uv = uv * grid_size;
    
    vec2 cell = floor(grid_uv);
 

    // DRAW THE PLAYER AND THE MOUSE AND THE SQUARES
    float r = step(abs(length(mouse_uv - uv)), circle_size);
    float g = step(abs(length(player_uv - uv)), circle_size);
    int value = map[int(grid_size.x * cell.x + cell.y)];
    float b = (1.0 - step(value, 0)) * step(r, 0.0) * step(g, 0.0) * step(view_all, 0.0);
    
    vec3 finalColor = vec3(r, g, b);


    if (r == 0.0 && g == 0.0) {
        // DRAW A LINE
        // vec3 finalColor = vec3(r, g, b);
        // if (line(player, mouse, invertedCoord, 0.5) == 1.0) {
        //     finalColor = vec3(1.0);
        // }

        if (lights_on == 1) {
            // DO THE RAY TRACING
            float max_dist_uv = ray_dist / grid_size.x;

            vec3 ray = ray_trace(player_grid_uv, grid_uv, ray_dist);
            float draw = ray.x;
            vec2 collision = ray.yz;

            // if (view_all == 1 && (0.1 > abs(length(grid_uv - collision)))) {
            if (view_all == 1 && (cell == (collision + vec2(1.0)))) {

                finalColor = vec3(0.0, 0.0, 1.0);

            } else if (draw == 1.0) {

                float minValue = 1.0 - max_dist_uv;
                float maxValue = 1.0;
                float d = 1.0 - abs(length(uv - player_uv));

                float mappedValue = (d - minValue) / (maxValue - minValue);
                float intensity = clamp(mappedValue, 0.0, 1.0);
                finalColor = vec3(intensity);

            }
            
        }

    }

    FragColor = vec4(finalColor, 1.0);

}
