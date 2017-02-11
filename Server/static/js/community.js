/**
 * Created by Kushan on 11-Feb-17.
 */

var loadCommunityGraph = function () {

    var width = 960,
        height = 500,
        radius = 10;

    var svg = d3.select("#network-graph").append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .gravity(0.5)
        .distance(200)
        .charge(-100)
        .size([width, height]);


    d3.json('/json/assets/nodes.json', function (json) {
        force
            .nodes(json.nodes)
            .links(json.links)
            .start();

        var min = Infinity
        var max = 0


        for (i = 0; i < json.nodes.length; i++) {
            degree = json.nodes[i].degree

            if (degree < min)
                min = degree

            if (degree > max)
                max = degree
        }


        var color = d3.scale.category20();


        var link = svg.selectAll(".link")
            .data(json.links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke-width", function (d) {
                return Math.sqrt(d.weight);
            });

        var node = svg.selectAll(".node")
            .data(json.nodes)
            .enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("circle")
            .attr("r", function (d) {
                return (((d.degree - min) / (max - min)) * (10 - 6)) + 6
            })
            .attr("fill", function (d) {
                return color(d.group)
            });

        node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function (d) {
                return
            });

        force.on("tick", function () {
            svg.selectAll("g.node")
                .attr("transform", function (d) {
                    d.x = Math.max(radius, Math.min(width - radius, d.x));
                    d.y = Math.max(radius, Math.min(height - radius, d.y));
                    return "translate(" + d.x + "," + d.y + ")";
                });

            link.attr("x1", function (d) {
                return d.source.x;
            })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });
        });
    });

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

}
