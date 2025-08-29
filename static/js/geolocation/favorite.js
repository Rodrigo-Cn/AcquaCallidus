function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function toggleFavorite(id) {
  try {
    const response = await fetch(`/geolocations/${id}/favorite/`, {
      method: "GET", 
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    });

    if (!response.ok) {
      throw new Error("Erro ao favoritar");
    }

    document.querySelectorAll('[id^="star-"] svg').forEach((svg) => {
      svg.setAttribute("fill", "none");
    });

    const currentStar = document.querySelector(`#star-${id} svg`);
    if (currentStar) currentStar.setAttribute("fill", "gold");

  } catch (error) {
    console.error(error);
  }
}

window.toggleFavorite = toggleFavorite;
