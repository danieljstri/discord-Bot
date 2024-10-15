import axios from 'axios';
const title = 'One Piece';

const baseUrl = 'https://api.mangadex.org';

const resp = await axios({
    method: 'GET',
    url: `${baseUrl}/manga`,
    params: {
        title: title
    }
});
const manga_ids = resp.data.data.map(manga => manga.id);

const resp_chapters = await axios({
    method: 'GET',
    url: `${baseUrl}/chapter`,
    params: {
        id: manga_ids[0]
    }
});

console.log(resp_chapters.data.data.map(chapter => chapter.attributes.chapter));