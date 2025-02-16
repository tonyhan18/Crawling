using PriceMap.Interfaces;

namespace PriceMap.Services;

public class SangaService : ISangaInterface
{
    private readonly IConfiguration _configuration;
    private readonly HttpClient _httpClient;
    public SangaService(IConfiguration configuration, HttpClient httpClient) 
    {
        this._configuration = configuration;
        this._httpClient = httpClient;
    }

    public async Task SangaCrawling(string keyword)
    {
        string baseUrl = _configuration["Naver:NaverSangaUrl"] + keyword;
        Console.WriteLine(baseUrl);
        var res = _httpClient.GetAsync(baseUrl).Result;
    }
}
