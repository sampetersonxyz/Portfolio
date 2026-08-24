

const isMobile = window.matchMedia("(max-width: 768px)").matches;

if (isMobile) {
    console.log("Mobile device detected");
} else {
    console.log("Desktop device detected");
}


function resizePage() {
    if (isMobile) {
        // Mobile layout
        console.log("Mobile layout");
        
    } else {
        // Desktop layout
        console.log("Desktop layout");
        // Change your page here
    }
}