// api/podcast.js
import { DOMParser } from "xmldom";

const url = "https://anchor.fm/s/49f0c604/podcast/rss";

async function fetchPodcastData(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Erro na requisição: ${response.status}`);
  }
  return response.text();
}

function parsePodcastData(xmlText) {
  const parser = new DOMParser();
  const xmlDoc = parser.parseFromString(xmlText, "text/xml");
  const items = xmlDoc.getElementsByTagName("item");

  return Array.from(items).map((item) => {
    const name =
      item.getElementsByTagName("title")[0]?.textContent ||
      "Título indisponível";
    const url =
      item.getElementsByTagName("enclosure")[0]?.getAttribute("url") ||
      "URL indisponível";

    return { name, url };
  });
}

async function getPodcastData() {
  try {
    const xmlText = await fetchPodcastData(url);
    const podcastData = parsePodcastData(xmlText);
    return podcastData;
  } catch (error) {
    console.error("Erro ao buscar dados do podcast:", error);
    return { error: error.message };
  }
}

export default async (req, res) => {
  const podcastData = await getPodcastData();
  res.setHeader("Access-Control-Allow-Origin", "https://24hb.vercel.app");
  res.status(200).json(podcastData);
};
