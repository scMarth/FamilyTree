// database query
fetch('/api/members')
  .then(res => res.json())
  .then(member_data => {
    console.log('member_data:', member_data);

    // Create a map from OBJECTID to NAME (to reference parents by ID)
    const idToName = {};
    member_data.forEach(person => {
      idToName[person.OBJECTID] = person.FIRST_NAME + ' ' + person.LAST_NAME;
    });

    // create nodes
    const nodes = member_data.map(person => ({
        id: person.FIRST_NAME + ' ' + person.LAST_NAME
    }));

    console.log('nodes:', nodes);

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

    console.log('links', links);

    // Select the SVG
    const svg = d3.select('svg');
    const width = window.innerWidth;
    const height = window.innerHeight;

    // Create simulation
    const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(150))
    .force('charge', d3.forceManyBody().strength(-400))
    .force('center', d3.forceCenter(width / 2, height / 2));

    // Draw links (lines between nodes)
    const link = svg.append('g')
    .attr('stroke', '#aaa')
    .selectAll('line')
    .data(links)
    .join('line')
    .attr('class', 'link');

    // Draw nodes (circles + labels)
    const node = svg.append('g')
    .selectAll('g')
    .data(nodes)
    .join('g')
    .attr('class', 'node');

    node.append('circle')
    .attr('r', 20)
    .attr('fill', 'steelblue');

    node.append('text')
    .text(d => d.id)
    .attr('dy', 4);

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

    console.log('end with d3?');
  });