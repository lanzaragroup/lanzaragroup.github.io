class MediaCarousel extends HTMLElement {
  templateElement = (description) => {
    let container = document.createElement('div');
    container.className = "item carousel-item";

    let child = null;
    if (description.video) {
      child = document.createElement('video');
      child.className = "d-block w-full carousel-video";
      child.setAttribute("loop", true);
      child.setAttribute("autoplay", true);
      child.setAttribute("playsinline", true);
      child.setAttribute("muted", true);

      let source = document.createElement('source');
      source.setAttribute("src", description.url);
      source.setAttribute("type", "video/mp4");
      child.appendChild(source);
    } else {
      child = document.createElement('img');
      child.className = "d-block w-100";
      child.setAttribute("src", description.url);
    }

    container.appendChild(child);

    return container;
  }

  rotate = () => {
    this.childElements[this.activeIndex].classList.remove("active");
    this.activeIndex = (this.activeIndex + 1) % this.childElements.length;
    this.childElements[this.activeIndex].classList.add("active");
    if (this.descriptions[this.activeIndex].video) {
      let video = this.childElements[this.activeIndex].querySelector("video");
      video.currentTime = 0;
    }
    setTimeout(() => this.rotate(), this.descriptions[this.activeIndex].interval);
  }

  constructor() {
    super();
    const template = document.getElementById("media-carousel-template");
    this.innerHTML = template.innerHTML;
    let root = this.querySelector(".carousel");

    this.descriptions = JSON.parse(this.dataset.items);
    this.childElements = this.descriptions.map(this.templateElement);

    this.activeIndex = this.childElements.length - 1;
    this.childElements.forEach(child => {
      root.appendChild(child);
    });

    this.rotate();
  }
}

class FundingAttribution extends HTMLElement {
  constructor() {
    super();
    const template = document.getElementById("funding-attribution-template");
    this.innerHTML = template.innerHTML;

    this.querySelector(".logo").setAttribute("src", this.dataset.img);
    this.querySelector(".agency").innerHTML = this.dataset.agency;
    this.querySelector(".grant").innerHTML = this.dataset.grant || "";
  }
}

class ResearchHighlight extends HTMLElement {
  constructor() {
    super();
    const template = document.getElementById("research-highlight-template");
    this.innerHTML = template.innerHTML;

    const highlight = JSON.parse(this.dataset.highlight);
    this.querySelector(".highlight-image").setAttribute("src",
      `${window.BASE_URL}/resource/highlights/${highlight.image_url}`);

    this.querySelector(".title").innerHTML = highlight.title;
    this.querySelector(".highlight-description").innerHTML = highlight.description;

    if (highlight.href) {
      this.querySelector(".pop-link").setAttribute("href", highlight.href);
    } else {
      this.querySelectorAll(".pop-link").style.display = "none";
    }

    this.querySelector(".paper-link").setAttribute("href", highlight.paper_href);
  }
}

class ShortPublication extends HTMLElement {
  constructor() {
    super();
    const template = document.getElementById("short-publication-template");
    this.innerHTML = template.innerHTML;

    const authors = JSON.parse(this.dataset.authors);
    console.log(this.dataset);

    this.querySelector(".title").innerHTML = this.dataset.title;
    this.querySelector(".authors").innerHTML = authors.join(", ");
    this.querySelector(".journal").innerHTML = this.dataset.journal;
    //this.querySelector(".year").innerHTML = this.dataset.year;
    this.querySelector(".title").setAttribute("href", this.dataset.href);
  }
}

class LabInitiative extends HTMLElement {
  constructor() {
    super();
    const template = document.getElementById("lab-initiative-template");
    this.innerHTML = template.innerHTML;
    this.querySelector(".initiative-link").href = this.dataset.href;
    this.querySelector(".initiative-title").textContent = this.dataset.title;
    this.querySelector(".initiative-image").setAttribute("src", this.dataset.image);
    this.querySelector(".initiative-content").innerHTML = this.dataset.content;
  }
}

class TeamMember extends HTMLElement {
  constructor() {
    super();
    const template = document.getElementById("team-member-template");
    this.innerHTML = template.innerHTML;
    this.querySelector(".name").innerHTML = this.dataset.name;
    this.querySelector(".portrait img").setAttribute("src", this.dataset.image);
    this.querySelector(".role").innerHTML = this.dataset.role;
    this.querySelector(".description").innerHTML = this.dataset.description;

    if (this.dataset.phone) {
      const pSpan = this.querySelector(".phone .number");
      pSpan.innerHTML = `${pSpan.innerHTML} (${this.dataset.phone})`;
    } else {
      this.querySelector(".phone").style.display = "none";
    }
    if (this.dataset.email) {
      const pSpan = this.querySelector(".email a");
      this.querySelector(".email .address").innerHTML = this.dataset.email;
      pSpan.href = `mailto:${this.dataset.email}`;

    } else {
      this.querySelector(".email").style.display = "none";
    }
    if (this.dataset.website) {
      const pSpan = this.querySelector(".website a");
      this.querySelector(".website .address").innerHTML = this.dataset.website;
      pSpan.href = this.dataset.website;
    } else {
      this.querySelector(".website").style.display = "none";
    }
  }
}

window.customElements.define("media-carousel", MediaCarousel);
window.customElements.define("lab-initiative", LabInitiative);
window.customElements.define("funding-attribution", FundingAttribution);
window.customElements.define("team-member", TeamMember);
window.customElements.define("short-publication", ShortPublication);
window.customElements.define("research-highlight", ResearchHighlight);

// ============= DROPDOWNS ====================

function setupDropdowns() {
  document.querySelectorAll(".dropdown-trigger").forEach(node => {
    node.addEventListener("click", function () {
      this.parentNode.parentNode.classList.toggle("closed");
    }, false);
  });
}


function setup() {
  setupDropdowns();
}

setup();
