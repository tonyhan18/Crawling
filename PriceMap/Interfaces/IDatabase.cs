using PriceMap.Models;

namespace PriceMap.Interfaces
{
    public interface IDatabase<T>
    {
        Task<List<T>> GetAsync();

        T GetDetail(int? id);

        void Create(T entity);

        void Update(int? id, T entity);

        void Delete(int? id);
    }
}
