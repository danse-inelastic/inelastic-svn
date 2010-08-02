background { rgb <1.000,1.000,1.000> }
camera{
 location <-1.119,2.926,5.186>
 look_at <-0.700,0.012,0.012>
}
light_source{
 <0.000,0.000,10.000>
 color rgb <1.000,1.000,1.000>
}
light_source{
 <0.000,0.000,-10.000>
 color rgb <1.000,1.000,1.000>
}
light_source{
 <0.000,10.000,0.000>
 color rgb <1.000,1.000,1.000>
}
light_source{
 <0.000,-10.000,0.000>
 color rgb <1.000,1.000,1.000>
}
light_source{
 <10.000,0.000,0.000>
 color rgb <1.000,1.000,1.000>
}
light_source{
 <-10.000,0.000,0.000>
 color rgb <1.000,1.000,1.000>
}
sphere{
 <0.000,0.000,0.000>,0.425
texture{
pigment {
 rgbt <0.439,0.502,0.565,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
sphere{
 <1.000,0.000,0.000>,0.300
texture{
pigment {
 rgbt <0.980,0.922,0.843,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
sphere{
 <-1.400,0.024,0.000>,0.425
texture{
pigment {
 rgbt <0.439,0.502,0.565,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
sphere{
 <-2.400,-0.000,0.024>,0.300
texture{
pigment {
 rgbt <0.980,0.922,0.843,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
cylinder{
 <0.000,0.000,0.000>, <0.500,0.000,0.000>, 0.100
 open
texture{
pigment {
 rgbt <0.439,0.502,0.565,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
cylinder{
 <0.500,0.000,0.000>, <1.000,0.000,0.000>, 0.100
 open
texture{
pigment {
 rgbt <0.980,0.922,0.843,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
cylinder{
 <0.000,0.000,0.000>, <-0.700,0.012,0.000>, 0.100
 open
texture{
pigment {
 rgbt <0.439,0.502,0.565,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
cylinder{
 <-0.700,0.012,0.000>, <-1.400,0.024,0.000>, 0.100
 open
texture{
pigment {
 rgbt <0.439,0.502,0.565,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
cylinder{
 <-1.400,0.024,0.000>, <-1.900,0.012,0.012>, 0.100
 open
texture{
pigment {
 rgbt <0.439,0.502,0.565,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
cylinder{
 <-1.900,0.012,0.012>, <-2.400,-0.000,0.024>, 0.100
 open
texture{
pigment {
 rgbt <0.980,0.922,0.843,0.000>
}
finish{
 ambient 0.20 diffuse 0.60 phong 1.00 specular 0.00
}
}
}
