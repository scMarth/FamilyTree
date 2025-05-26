// database query
fetch('/FamilyTree/api/members')
  .then(res => res.json())
  .then(member_data => {

    // Create a map from OBJECTID to NAME (to reference parents by ID)
    const idToName = {};
    member_data.forEach(person => {
      idToName[person.OBJECTID] = person.FIRST_NAME + ' ' + person.LAST_NAME;
    });

    // create nodes
    const nodes = member_data.map(person => ({
        id: person.FIRST_NAME + ' ' + person.LAST_NAME
    }));

    // create links
    const links = [];
    member_data.forEach(person => {
        if (person.MOTHER !== null) {
          links.push({
            source: idToName[person.MOTHER],
            target: person.FIRST_NAME + ' ' + person.LAST_NAME
          });
        }
        if (person.FATHER !== null) {
          links.push({
            source: idToName[person.FATHER],
            target: person.FIRST_NAME + ' ' + person.LAST_NAME
          });
        }
    });

    // Select the SVG
    const svg = d3.select('svg');
    const g = svg.append("g");

    // Enable zoom & pan
    const zoom = d3.zoom()
      .scaleExtent([0.1, 3]) // optional: min and max zoom scale
      .on("zoom", (event) => {
        g.attr("transform", event.transform); // apply zoom/pan to the group
      });

    svg.call(zoom);

    const width = window.innerWidth;
    const height = window.innerHeight;

    // Create simulation
    const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(150))
    .force('charge', d3.forceManyBody().strength(-400))
    .force('center', d3.forceCenter(width / 2, height / 2));

    // Draw links (lines between nodes)
    const link = g.selectAll('.link')
      .data(links)
      .join('line')
      .attr('class', 'link')
      .attr('stroke', '#aaa');

    // Draw nodes (circles + labels)
    const node = g.selectAll('.node')
      .data(nodes)
      .join('g')
      .attr('class', 'node');

    node.append('circle')
    .attr('r', 20)
    .attr('fill', 'steelblue');

    node.append('text')
    .text(d => d.id)
    .attr('dy', 4)
    .attr('text-anchor', 'middle');

    // Update positions on each tick
    simulation.on('tick', () => {
    link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

    node
        .attr('transform', d => `translate(${d.x},${d.y})`);
    });
  });