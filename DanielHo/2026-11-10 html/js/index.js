// Search Function
document.getElementById("searchButton").addEventListener("click", () => {
    const query = document.getElementById("exampleDataList").value;

    if (!query.trim()) {
        alert("Please enter a recipe name.");
        return;
    }

    window.location.href = `/recipes?search=${encodeURIComponent(query)}`;
});
