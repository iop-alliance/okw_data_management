function createClusterIcon_b(cluster) {
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

function createClusterIcon(cluster) {
    var childCount = cluster.getChildCount();
    var size = 30; // Default size
    var opacity = 0.8;
    var text = '';
    var color = '#1E90FF'; // Default color

    // Define an enhanced color scale
    var colors = [
    "#1f8fff",
    "#2757ff",
    "#3d30ff",
    "#7d38ff",
    "#b841ff",
    "#ee49ff",
    "#ff52de",
    "#ff5ab1",
    "#ff6389",
    "#ff706b"
    ];

    // Set text and color based on child count
    if (childCount === 1) {
        text = ''; // No text for a single item
        color = colors[0]; // Dodger Blue for a single point
    } else if (childCount >= 2 && childCount <= 5) {
        color = colors[1]; // Light Blue for most points
    } else if (childCount >= 5 && childCount <= 20) {
        size = 25;
        color = colors[2]; // Light Purple
    } else if (childCount >= 20 && childCount <= 50) {
        size = 30;
        color = colors[3]; // Medium Pink
    } else if (childCount >= 50 && childCount <= 100) {
        size = 30;
        color = colors[4]; // Hot Pink
    } else if (childCount >= 100 && childCount <= 300) {
        size = 35;
        color = colors[5]; // Coral Red
    } else if (childCount >= 300 && childCount <= 500) {
        size = 35;
        color = colors[6]; // Bright Red
    } else if (childCount >= 500 && childCount <= 1000) {
        size = 35;
        color = colors[7]; // Bright Red
    } else if (childCount >= 1000 && childCount <= 2000) {
        size = 35;
        color = colors[8]; // Bright Red
    } else if (childCount > 2000) {
        size = 40;
        color = colors[9]; // Firebrick Red for max value
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
