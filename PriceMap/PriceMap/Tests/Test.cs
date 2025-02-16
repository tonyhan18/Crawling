using Xunit;
using PriceMap.Services;
using PriceMap.Interfaces;
using Microsoft.Extensions.Configuration;

namespace PriceMap.Tests
{
    public class Test
    {
        private readonly SangaService _service;
        private readonly IConfiguration _configuration;

        public Test()
        {
            //var configurationBuilder = new ConfigurationBuilder();
            var initialData = new Dictionary<string, string>
                {
                    {"Naver:NaverSangaUrl", "https://m.land.naver.com/search/result/"}
                };
            //configurationBuilder.Add(new MemoryConfigurationSource { InitialData = initialData });
            _configuration = new ConfigurationBuilder()
                .AddInMemoryCollection(initialData).Build();
            _service = new SangaService(_configuration);
        }
        [Fact]
        public void RunSangaCrawling()
        {
            _service.SangaCrawling("구로구 구로동");
        }
    }
}
