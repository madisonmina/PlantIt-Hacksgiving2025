let draggedPlant = null;

document.querySelectorAll('.plant').forEach(item => {
  item.addEventListener('dragstart', () => {
    draggedPlant = item.getAttribute('data-name');
  });
});

document.querySelectorAll('.region').forEach(region => {
  region.addEventListener('dragover', e => e.preventDefault());

  region.addEventListener('drop', e => {
    region.style.fill = getRandomColor();
    region.style.opacity = 0.6;

    // Add text label
    const label = document.createElementNS("http://www.w3.org/200/svg", "text");
    label.setAttribute("x", e.offsetX);
    label.setAttribute("y", e.offsetY);
    label.textContent = draggedPlant;
    label.setAttribute("font-size", "20");
    label.setAttribute("fill", "black");

    region.parentNode.appendChild(label);
  });
});

// helper function for colors
function getRandomColor() {
  return "hsl(" + Math.random() * 360 + ", 60%, 65%)";
}
