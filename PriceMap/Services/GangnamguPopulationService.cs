using PriceMap.Interfaces;
using PriceMap.Models;
using Humanizer.DateTimeHumanizeStrategy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace PriceMap.Services
{
    public class GangnamguPopulationService : IDatabase<GangnamguPopulation>
    {
        private readonly BlazorServerDbContext? _context;

        public GangnamguPopulationService(BlazorServerDbContext context)
        {
            this._context = context;
        }

        public void Create(GangnamguPopulation entity)
        {
            if (_context?.GangnamguPopulations == null) 
            {
                throw new NullReferenceException();
            }

            this._context.GangnamguPopulations.Add(entity);
            this._context?.SaveChanges();        
        }

        public void Delete(int? id)
        {
            if (_context?.GangnamguPopulations == null)
            {
                throw new NullReferenceException();
            }

            var validData = this._context.GangnamguPopulations.Find(id);

            if (validData != null)
            {
                this._context.GangnamguPopulations.Remove(validData);
                this._context.SaveChanges();
            }
        }

        public async Task<List<GangnamguPopulation>> GetAsync()
        {
            return await this._context.GangnamguPopulations.ToListAsync();
        }

        public GangnamguPopulation GetDetail(int? id)
        {
            if (id == null || _context?.GangnamguPopulations == null)
            {
                throw new NullReferenceException();
            }

            var validData = this._context.GangnamguPopulations.FirstOrDefault(x => x.Id == id);

            if (validData != null)
            {
                return validData;
            }
            else 
            {
                throw new InvalidOperationException();
            }
        }

        public void Update(int? id, GangnamguPopulation entity)
        {
            if (id == null || _context?.GangnamguPopulations == null)
            {
                throw new NullReferenceException();
            }

            var validData = this._context.GangnamguPopulations.FirstOrDefault(x => x.Id == id);
            
            if (validData != null)
            {
                this._context.GangnamguPopulations.Update(entity);
                this._context.SaveChanges();
            }
            else
            {
                throw new InvalidOperationException();
            }
        }
    }
}
