const axios = require('axios');
const cheerio = require('cheerio');

// Função para buscar os capítulos de um mangá no MangaFox
async function getMangaChapters(mangaSlug) {
    try {
        // Faz uma requisição GET para a página do mangá no MangaFox
        const response = await axios.get(`https://mangafox.site/manga/${mangaSlug}`);
        
        // Carrega o HTML retornado
        const $ = cheerio.load(response.data);
        
        // Array para armazenar os capítulos
        const chapters = [];
        
        // Encontra todos os elementos <a> com a classe "chapter-link"
        $('a.chapter-link').each((index, element) => {
            // Extrai o título e a URL do capítulo
            const title = $(element).text().trim();
            const url = $(element).attr('href');
            
            // Adiciona o capítulo ao array
            chapters.push({ title, url });
        });
        
        // Retorna a lista de capítulos
        return chapters;
    } catch (error) {
        console.error('Erro ao buscar capítulos:', error);
        return [];
    }
}

// Exemplo de uso
const mangaSlug = 'kingdom'; // Substitua pelo slug do mangá desejado
getMangaChapters(mangaSlug)
    .then(chapters => {
        console.log('Capítulos encontrados:');
        chapters.forEach(chapter => {
            console.log(`${chapter.title}: ${chapter.url}`);
        });
    })
    .catch(error => {
        console.error('Erro:', error);
    });
