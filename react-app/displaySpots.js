<script src="https://d3js.org/d3.v5.js"></script>

d3.json("data.json", function(data){
    var svg = d3.select("svg")

    var rect = d3.selectAll('rect');

    var spotEnter = spot.enter()
        .append('rect')
        .attr('x', function(d){ return d.x * 100})
        .attr('y', function(d){ return d.y * 50})
        .attr('width', 100)
        .attr('height', 50);
});