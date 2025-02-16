using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace PriceMap.Services;

public class HttpService
{
    private readonly HttpClient _httpClient;

    public HttpService(HttpClient httpClient)
    {
        _httpClient = httpClient;
    }

    public async Task<string> GetAsync(string url)
    {
        var response = await _httpClient.GetAsync(url);
        return await HandleResponse(response);
    }

    // POST 요청
    public async Task<string> PostAsync(string url, string jsonData)
    {
        var content = new StringContent(jsonData, Encoding.UTF8, "application/json");
        var response = await _httpClient.PostAsync(url, content);
        return await HandleResponse(response);
    }

    // PUT 요청
    public async Task<string> PutAsync(string url, string jsonData)
    {
        var content = new StringContent(jsonData, Encoding.UTF8, "application/json");
        var response = await _httpClient.PutAsync(url, content);
        return await HandleResponse(response);
    }

    // DELETE 요청
    public async Task<string> DeleteAsync(string url)
    {
        var response = await _httpClient.DeleteAsync(url);
        return await HandleResponse(response);
    }

    // HTTP 응답 처리
    private async Task<string> HandleResponse(HttpResponseMessage response)
    {
        if (response.IsSuccessStatusCode)
        {
            return await response.Content.ReadAsStringAsync();
        }
        else
        {
            throw new HttpRequestException($"Error: {response.StatusCode}, {await response.Content.ReadAsStringAsync()}");
        }
    }
}
