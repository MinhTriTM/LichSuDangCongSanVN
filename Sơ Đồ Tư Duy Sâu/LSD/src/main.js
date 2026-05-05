import * as d3 from 'd3';

const container = document.getElementById('mindmap-container');
let width = container.clientWidth;
let height = container.clientHeight;

const svg = d3.select("#mindmap-container")
  .append("svg")
  .attr("width", width)
  .attr("height", height)
  .attr("viewBox", [0, 0, width, height]);

const g = svg.append("g");

const zoom = d3.zoom()
  .scaleExtent([0.1, 3])
  .on("zoom", (event) => {
    g.attr("transform", event.transform);
  });

svg.call(zoom);

const tooltip = d3.select("#tooltip");

let root;
let i = 0;
const duration = 750;
let dx = 40;
let dy = 280;
const tree = d3.tree().nodeSize([dx, dy]);
const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

d3.json("/data/mindmap.json").then(data => {
  root = d3.hierarchy(data);
  root.x0 = height / 2;
  root.y0 = 0;
  
  root.descendants().forEach((d, i) => {
    d.id = i;
    d._children = d.children;
  });
  
  // Thu gọn ngay từ level 1 (children của root)
  if (root.children) {
    root.children.forEach(collapse);
  }

  update(root);
  
  svg.transition().duration(duration).call(
    zoom.transform, 
    d3.zoomIdentity.translate(width / 6, height / 2).scale(0.8)
  );
}).catch(error => {
  console.error("Error loading data:", error);
});

function collapse(d) {
  if (d.children) {
    d._children = d.children;
    d._children.forEach(collapse);
    d.children = null;
  }
}

function expand(d) {
  if (d._children) {
    d.children = d._children;
    d.children.forEach(expand);
    d._children = null;
  } else if (d.children) {
    d.children.forEach(expand);
  }
}

function update(source) {
  const nodes = root.descendants().reverse();
  const links = root.links();
  
  tree(root);

  let left = root;
  let right = root;
  root.eachBefore(node => {
    if (node.x < left.x) left = node;
    if (node.x > right.x) right = node;
  });

  const node = g.selectAll("g.node")
    .data(nodes, d => d.id);

  const nodeEnter = node.enter().append("g")
    .attr("class", "node")
    .attr("transform", d => `translate(${source.y0},${source.x0})`)
    .on("click", (event, d) => {
      d.children = d.children ? null : d._children;
      update(d);
    })
    .on("mouseover", (event, d) => {
      if (d.data.details) {
        tooltip.transition().duration(200).style("opacity", .95);
        tooltip.html(`<strong>${d.data.name}</strong>${d.data.details}`)
          .style("left", (event.pageX + 15) + "px")
          .style("top", (event.pageY - 28) + "px");
      }
    })
    .on("mouseout", () => {
      tooltip.transition().duration(500).style("opacity", 0);
    });

  nodeEnter.append("circle")
    .attr("r", 1e-6)
    .style("fill", d => d._children ? "#da251d" : "#fff");

  nodeEnter.append("text")
    .attr("dy", "0.31em")
    .attr("x", d => d._children ? -10 : 10)
    .attr("text-anchor", d => d._children ? "end" : "start")
    .text(d => d.data.name)
    .clone(true).lower()
    .attr("stroke-linejoin", "round")
    .attr("stroke-width", 3)
    .attr("stroke", "white");

  const nodeUpdate = nodeEnter.merge(node);

  nodeUpdate.transition()
    .duration(duration)
    .attr("transform", d => `translate(${d.y},${d.x})`);

  nodeUpdate.select("circle")
    .attr("r", 6)
    .style("fill", d => d._children ? "#da251d" : "#fff")
    .style("stroke", d => d._children ? "#da251d" : "#da251d");

  const nodeExit = node.exit().transition()
    .duration(duration)
    .attr("transform", d => `translate(${source.y},${source.x})`)
    .remove();

  nodeExit.select("circle").attr("r", 1e-6);
  nodeExit.select("text").style("fill-opacity", 1e-6);

  const link = g.selectAll("path.link")
    .data(links, d => d.target.id);

  const linkEnter = link.enter().insert("path", "g")
    .attr("class", "link")
    .attr("d", d => {
      const o = {x: source.x0, y: source.y0};
      return diagonal({source: o, target: o});
    });

  const linkUpdate = linkEnter.merge(link);

  linkUpdate.transition()
    .duration(duration)
    .attr("d", diagonal);

  link.exit().transition()
    .duration(duration)
    .attr("d", d => {
      const o = {x: source.x, y: source.y};
      return diagonal({source: o, target: o});
    })
    .remove();

  nodes.forEach(d => {
    d.x0 = d.x;
    d.y0 = d.y;
  });
}

// UI Controls
document.getElementById('btn-zoom-in').addEventListener('click', () => {
  svg.transition().call(zoom.scaleBy, 1.3);
});

document.getElementById('btn-zoom-out').addEventListener('click', () => {
  svg.transition().call(zoom.scaleBy, 0.7);
});

document.getElementById('btn-center').addEventListener('click', () => {
  svg.transition().duration(duration).call(
    zoom.transform, 
    d3.zoomIdentity.translate(width / 6, height / 2).scale(0.8)
  );
});

document.getElementById('btn-collapse-all').addEventListener('click', () => {
  if (root.children) {
    root.children.forEach(collapse);
    update(root);
    svg.transition().duration(duration).call(
      zoom.transform, 
      d3.zoomIdentity.translate(width / 6, height / 2).scale(0.8)
    );
  }
});

document.getElementById('btn-expand-all').addEventListener('click', () => {
  expand(root);
  update(root);
});

window.addEventListener('resize', () => {
  width = container.clientWidth;
  height = container.clientHeight;
  svg.attr("width", width).attr("height", height).attr("viewBox", [0, 0, width, height]);
});