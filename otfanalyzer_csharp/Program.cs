using System;

namespace otfanalyzer_csharp
{
    class Program
    {
        static void showUsage(string programName)
        {
            System.Console.WriteLine("[usage] {0} OTF_PATH\n", programName);
        }

        static void Main(string[] args)
        {
            if ( args.Length < 1 )
            {
                showUsage(Environment.GetCommandLineArgs()[0]);
                return;
            }
        }
    }
}
