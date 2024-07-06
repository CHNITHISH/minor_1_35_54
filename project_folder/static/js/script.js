document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript loaded");

    // Example interaction: Change the border color of the video feed on hover
    const videoElement = document.getElementById('video');
    
    videoElement.addEventListener('mouseover', function() {
        videoElement.style.borderColor = '#00ff00';  // Change to green on hover
    });

    videoElement.addEventListener('mouseout', function() {
        videoElement.style.borderColor = '#ccc';  // Change back to default on mouse out
    });

    // Example: Show a message when the video feed is clicked
    videoElement.addEventListener('click', function() {
        alert("Video feed clicked!");
    });
});
