function createClusterIcon(cluster) {
    var childCount = cluster.getChildCount();
    var size = 20; // Default size
    var opacity = 0.8;
    var text = '';
    var color = '#1E90FF'; // Default color
    var colors = ['#1E90FF', '#69B4FF', '#B469FF', '#FF69FF', '#FF69B4', '#FF6F69'];

    // Set text and color based on child count
    if (childCount === 1) {
        text = ''; // No text for a single item
        color = colors[0];
    } else if (childCount >= 2 && childCount <= 5) {
        color = colors[0];
    } else if (childCount >= 5 && childCount <= 20) {
        size = 25;
        color = colors[2];
    } else if (childCount >= 20 && childCount <= 100) {
        size = 30;
        color = colors[3];
    } else if (childCount >= 100 && childCount <= 500) {
        size = 30;
        color = colors[4];
    } else if (childCount > 500) {
        size = 35;
        color = colors[5];
    }

    // Set text if childCount > 1
    if (childCount > 1) {
        text = `<span style="font-family: 'Fira Mono', monospace; font-weight: 500; font-style: normal;">${childCount}</span>`;
    }

    // Return the cluster icon
    return new L.DivIcon({
        html: `<div style="background-color:${color}; height:${size}px; width:${size}px; opacity:${opacity}; border-radius: 10%; display: flex; align-items: center; justify-content: center; text-align: center;">${text}</div>`,
        className: '',
        iconSize: new L.Point(size, size)
    });
}
