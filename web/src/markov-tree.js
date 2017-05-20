var margin = {top: 0, right: 50, bottom: 120, left: 77},
    width = screen.width - margin.right - margin.left,
    height = screen.height - margin.top - margin.bottom;

var i = 0,
    duration = 750,
    root;

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });


var svg = d3.select("body").append("svg")
    .attr("width",function() {
        return  "100%";})
        
        // return  width + margin.right + margin.left;})
        //return  width + margin.right + margin.left;})
    .attr("height", function(){
        // return height + margin.top + margin.bottom;})
        return "100%"; })
        // return height + margin.top + margin.bottom; })
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var tree = d3.layout.tree()
    .size([height, width]);

var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);

// d3.json("data/chain.json", function(error, tree) {
//     if (error) {
//         root = json;
//     }
    root = json;
    root.name = "S";
    root.probability = 1;
    root.x0 = height / 2;
    root.y0 = 0;

    function collapse(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    root.children.forEach(collapse);
    update(root);


//});

function update(source) {

    // Compute the new tree layout.
    var nodes = tree.nodes(root),
    links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function(d) { d.y = d.depth * 180; });
    //nodes.forEach(function(d) { d.y = d.depth * 180; });

    // Update the nodes…
    var node = svg.selectAll("g.node")
        .data(nodes, function(d) { return d.id || (d.id = ++i); });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) {
            return "translate(" + source.y0 + "," + source.x0 + ")"; })
        .on("click", click);

    nodeEnter
        .filter(function(d){ return d.accept; })
        .on("mouseover", function(d) {            
            div.transition()		
                .duration(200)		
                .style("opacity", .9);		
            div.html(d.word)
	        .style("right",  "2px")		
                .style("bottom", "50%");
            })					
        .on("mouseout", function(d) {		
            div.transition()		
                .duration(500)		
                .style("opacity", 0);	
        });

    
    nodeEnter.append("circle")
        .attr("class", "outer")
        .attr("r", 1e-6)
        .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

    nodeEnter
        .filter(function(d) {return d.accept;})
        .append("circle")
        .attr("class", "inner")
        .style("fill", function(d) {
            return d._children ? "lightsteelblue" : "#fff";
        });
    
    nodeEnter.append("text")
        .attr("class", "name")
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")
        .text(function(d) { return d.name; })
        .style("fill-opacity", 1e-6);

    nodeEnter.append("text")
        .attr("class", "frequency")
        .attr("x", function(d) { return d.children || d._children ? -80 : 35; }) // -40 20
        .attr("dy", ".35em")
        .attr("text-anchor", "start")
        .text(function(d) { return d.probability.toFixed(2); });

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

    nodeUpdate.select("circle.outer")
        .attr("r", 30)
        .style("fill", function(d) {          
            return d._children ? "lightsteelblue" : "#fff";
        });

    nodeUpdate.select("circle.inner")
        .attr("r", 26)
        .style("fill", function(d) {          
            return d._children ? "lightsteelblue" : "#fff";
        });;

    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform",
              function(d) { return "translate(" + source.y + "," + source.x + ")"; })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links…
    var link = svg.selectAll("path.link")
        .data(links, function(d) { return d.target.id; });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function(d) {
            var o = {x: source.x0, y: source.y0};
            return diagonal({source: o, target: o});
        })
        .style("stroke-width", function(d) {
            return 1.5 + (10 * d.target.probability);
        });

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function(d) {
            var o = {x: source.x, y: source.y};
            return diagonal({source: o, target: o});
        })
        .remove();
    
    // Stash the old positions for transition.
    nodes.forEach(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

// function words(words) {
//     if (d.children) {
//         return words.concat(words(d.children));
//     } else {
//     }
//     mouseover(d);

    
//     var info = d3.select("div#info");
//     info.selectAll("*").remove();
//     if (d.accept == true){
//         console.log(d.word);
//         info.append("h1").text(d.word);
//     }

// }

// Toggle children on click.
function click(d) {
    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
    update(d);
}
