/**
 * Created by Kushan on 11-Feb-17.
 */

var loadCommunityGraph = function () {

    var width = 700,
        height = 400,
        radius = 10;

    var svg = d3.select("#network-graph").append("svg")
        .attr("width", width)
        .attr("height", height);
    //Set up tooltip
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function (d) {
            return d.user_id + "";
        });
    svg.call(tip);

    var force = d3.layout.force()
        .gravity(.05)
        .charge(-240)
        .linkDistance(100)
        .size([width, height]);


    d3.json('/json/assets/nodes_' + course_id + '.json?_=' + new Date().getTime(), function (json) {
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
            .call(force.drag)
            .on('mouseover', tip.show) //Added
            .on('mouseout', tip.hide); //Added ;

        node.append("circle")
            .attr("r", function (d) {
                if (d.degree == 0)
                    return 0
                else
                    return (((d.degree - min) / (max - min)) * (20 - 6)) + 6
            })
            .attr("fill", function (d) {
                if (d.degree == 0)
                    return
                else
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
            node.attr("cx", function (d) {
                return d.x;
            })
                .attr("cy", function (d) {
                    return d.y;
                });
            node.each(collide(0.5)); //Added
        });

        var padding = 1, // separation between circles
            radius = 8;

        function collide(alpha) {
            var quadtree = d3.geom.quadtree(json.nodes);
            return function (d) {
                var rb = 2 * radius + padding,
                    nx1 = d.x - rb,
                    nx2 = d.x + rb,
                    ny1 = d.y - rb,
                    ny2 = d.y + rb;
                quadtree.visit(function (quad, x1, y1, x2, y2) {
                    if (quad.point && (quad.point !== d)) {
                        var x = d.x - quad.point.x,
                            y = d.y - quad.point.y,
                            l = Math.sqrt(x * x + y * y);
                        if (l < rb) {
                            l = (l - rb) / l * alpha;
                            d.x -= x *= l;
                            d.y -= y *= l;
                            quad.point.x += x;
                            quad.point.y += y;
                        }
                    }
                    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                });
            };
        }


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
