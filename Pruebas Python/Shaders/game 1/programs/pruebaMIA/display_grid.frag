#version 460 core   



uniform vec2 resolution; 
uniform float time; // Time uniform variable for animation

uniform int lights_on;
uniform int view_all;
uniform vec2 player;
uniform vec2 mouse;

// const uniform vec2 grid_size;
// const int max_marked_squares = grid_size.x * grid_size.y;
// uniform int num_marked_squares;
// uniform int marked_squares[max_marked_squares];

// uniform int map[grid_size.x][grid_size.y];


void main() {
    // vec2 cell = floor(gl_FragCoord.xy / grid_size.xy);

    // vec3 color = vec3(mod(cell.x + cell.y, 2.0));

    float a = sin(time);
    float b = sin(time + 3.14);
    float c = sin(time + 3.14 / 2.0);
    vec3 color = vec3(a, b, c);

    gl_FragColor = vec4(color, 1.0);
}







const vec2 grid_size = vec2(3, 3);
const int max_marked_squares = 9;
const int num_marked_squares = 2;

vec2 marked_squares[max_marked_squares];


int numElements = 0;
void addElement(vec2 newElement) {
    if (numElements < max_marked_squares) {
        marked_squares[numElements] = newElement;
        numElements++;
    }
}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    addElement(vec2(1.0, 2.0));

    vec2 cell = floor(fragCoord.xy * grid_size.xy / iResolution.xy);
    cell.y = grid_size.y - 1.0 - cell.y;


    vec3 color = vec3(0.0);
    for (int i = 0; i < num_marked_squares; i++) {
        if (marked_squares[i] == cell) {
            color = vec3(0.0, 0.0, 1.0);
        }
    }


    fragColor = vec4(color,1.0);
}