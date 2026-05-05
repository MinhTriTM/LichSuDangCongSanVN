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

let root;
const duration = 750;
let dx = 80; // Tăng khoảng cách dọc để Box to không đè nhau
let dy = 450; // Tăng khoảng cách ngang
const tree = d3.tree().nodeSize([dx, dy]);
const diagonal = d3.linkHorizontal().x(d => d.y).y(d => d.x);

function processRawTracNghiem(rawData) {
  const processedRoot = {
    name: "BỘ ĐỀ TRẮC NGHIỆM LỊCH SỬ ĐẢNG (1131 CÂU)",
    details: "Toàn bộ dữ liệu trắc nghiệm được hệ thống hóa sâu 8 tầng.",
    children: []
  };

  if (Array.isArray(rawData)) {
    const chunkNode = { name: "Tất cả câu hỏi", children: [] };
    const chunkSize = 20; // 20 câu 1 nhánh
    for (let i = 0; i < rawData.length; i += chunkSize) {
      const chunk = rawData.slice(i, i + chunkSize);
      const groupNode = { name: `Nhóm ${i + 1} - ${i + chunk.length}`, children: [] };
      chunk.forEach(q => {
        groupNode.children.push({
          name: (q.question || "").substring(0, 40) + "...",
          question: q.question,
          options: q.options,
          answer: q.answer
        });
      });
      chunkNode.children.push(groupNode);
    }
    processedRoot.children.push(chunkNode);
  } else if (typeof rawData === 'object') {
    for (const [chuong, qList] of Object.entries(rawData)) {
      const chuongNode = { name: chuong, children: [] };
      const chunkSize = 20;
      for (let i = 0; i < qList.length; i += chunkSize) {
        const chunk = qList.slice(i, i + chunkSize);
        const groupNode = { name: `Nhóm ${i + 1} - ${i + chunk.length}`, children: [] };
        chunk.forEach(q => {
          groupNode.children.push({
            name: (q.question || "").substring(0, 40) + "...",
            question: q.question,
            options: q.options,
            answer: q.answer
          });
        });
        chuongNode.children.push(groupNode);
      }
      processedRoot.children.push(chuongNode);
    }
  }
  return processedRoot;
}

function loadData(url) {
  // Clear old map
  g.selectAll("*").remove();

  // Kiểm tra nếu là file trắc nghiệm thô ở thư mục cha
  const isRawTracNghiem = url === '../tracnghiem_LSD_chuong_gemini.json';

  d3.json(url).then(data => {
    let treeData = data;
    if (isRawTracNghiem) {
      treeData = processRawTracNghiem(data);
    }

    root = d3.hierarchy(treeData);
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
    alert(`Lỗi tải dữ liệu từ ${url}. Hãy chắc chắn Web Server đang chạy và file tồn tại.`);
  });
}

// Khởi tạo dataset mặc định
loadData("data/timeline.json");

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
      // Chỉ collapse/expand nếu có nhánh con
      if (d.children || d._children) {
        d.children = d.children ? null : d._children;
        update(d);
      }
    });

  // Vẽ hình tròn cho các Node CÓ chứa nhánh con
  nodeEnter.filter(d => d._children || d.children)
    .append("circle")
    .attr("r", 1e-6)
    .style("fill", d => d._children ? "var(--primary)" : "#fff")
    .style("stroke", "var(--primary)");

  // Vẽ Text cho các Node CÓ chứa nhánh con
  nodeEnter.filter(d => d._children || d.children)
    .append("text")
    .attr("dy", "0.31em")
    .attr("x", d => d._children ? -12 : 12)
    .attr("text-anchor", d => d._children ? "end" : "start")
    .text(d => d.data.name)
    .clone(true).lower()
    .attr("stroke-linejoin", "round")
    .attr("stroke-width", 3)
    .attr("stroke", "white");

  // Vẽ Thẻ Text Box hiện vĩnh viễn (foreignObject) cho Node lá (KHÔNG có con)
  const leafNodes = nodeEnter.filter(d => !d._children && !d.children);
  
  leafNodes.append("foreignObject")
    .attr("width", 380)
    .attr("height", 240)
    .attr("x", 15)
    .attr("y", -120)
    .style("opacity", 0)
    .append("xhtml:div")
    .attr("class", "node-box")
    .html(d => `
      <h4>${d.data.name}</h4>
      <p>${d.data.details || d.data.question || "Không có thông tin chi tiết."}</p>
      ${d.data.options ? `<br><i>${d.data.options.join('<br>')}</i>` : ''}
      ${d.data.answer ? `<br><b>Đ/A: ${d.data.answer}</b>` : ''}
    `);

  const nodeUpdate = nodeEnter.merge(node);

  nodeUpdate.transition()
    .duration(duration)
    .attr("transform", d => `translate(${d.y},${d.x})`);

  nodeUpdate.select("circle")
    .attr("r", 7)
    .style("fill", d => d._children ? "var(--primary)" : "#fff");

  nodeUpdate.select("foreignObject")
    .style("opacity", 1)
    .attr("height", 240);

  const nodeExit = node.exit().transition()
    .duration(duration)
    .attr("transform", d => `translate(${source.y},${source.x})`)
    .remove();

  nodeExit.select("circle").attr("r", 1e-6);
  nodeExit.select("text").style("fill-opacity", 1e-6);
  nodeExit.select("foreignObject").style("opacity", 1e-6);

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
  if (root && root.children) {
    root.children.forEach(collapse);
    update(root);
    svg.transition().duration(duration).call(
      zoom.transform, 
      d3.zoomIdentity.translate(width / 6, height / 2).scale(0.8)
    );
  }
});

document.getElementById('btn-expand-all').addEventListener('click', () => {
  if (root) {
    expand(root);
    update(root);
  }
});

window.addEventListener('resize', () => {
  width = container.clientWidth;
  height = container.clientHeight;
  svg.attr("width", width).attr("height", height).attr("viewBox", [0, 0, width, height]);
});

// Chuyển đổi Dataset
document.querySelectorAll('.dataset-btn').forEach(btn => {
  btn.addEventListener('click', (e) => {
    document.querySelectorAll('.dataset-btn').forEach(b => b.classList.remove('active'));
    e.target.classList.add('active');
    
    let url = e.target.getAttribute('data-file');
    // Đổi logic load file trắc nghiệm trỏ thẳng về thư mục gốc
    if (url === 'data/tracnghiem.json') {
        url = '../tracnghiem_LSD_chuong_gemini.json';
    }
    loadData(url);
  });
});