using Newtonsoft.Json;
using System;
using System.Diagnostics;
//using Newtonsoft.Json;
using System.Text.Json;


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

        /// <summary>
        /// List Type의 결과를 반환하는 Python Script를 실행합니다.
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="scriptPath"></param>
        /// <param name="args"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>
        public async Task<List<T>?> RunScriptListAsync<T>(string scriptPath, string args = "")
        {
            Console.WriteLine("On Work");
            Console.WriteLine(scriptPath);
            List<T>? result = new List<T>();
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

                //result = JsonConvert.DeserializeObject<List<T>>(output);

                return result;
            }
        }

        public async Task<string> RunScriptAsync(string scriptPath, string args = "")
        {
            string? result;
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

                result = JsonConvert.DeserializeObject<string>(output);

                return result;
            }
        }
    }
}