using System;
using System.Diagnostics;
using System.Threading.Tasks;

namespace PriceMap.Python
{
    public class PythonRunner
    {
        private readonly ProcessStartInfo _psi;

        public PythonRunner()
        {
            _psi = new ProcessStartInfo
            {
                FileName = "python",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
        }

        public async Task<string> RunScriptAsync(string scriptPath, string args = "")
        {
            _psi.Arguments = $"{scriptPath} {args}";

            using (Process process = new Process { StartInfo = _psi })
            {
                process.Start();

                string output = await process.StandardOutput.ReadToEndAsync();
                string error = await process.StandardError.ReadToEndAsync();

                await process.WaitForExitAsync();

                if (process.ExitCode != 0)
                {
                    throw new Exception($"Python script exited with error: {error}");
                }

                return output;
            }
        }
    }
}