using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace get_filename
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void openfolder(object sender, EventArgs e)
        {
            FolderBrowserDialog diag = new FolderBrowserDialog();
            if (diag.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                string folder = diag.SelectedPath;  //selected folder path
                txt1.Text = folder;
            }
        }

        private void export_to_csv(object sender, EventArgs e)
        {
            var filename = txt_url.Text +  @"\StudentID.csv";
            FileStream fs = File.Create(filename);
            string path = txt1.Text;
            string[] dr = Directory.GetDirectories(path);
            StreamWriter writer = new StreamWriter(fs);
            foreach (string s in dr)

            try
            {
                    string name = s.Remove(0, s.LastIndexOf('\\') + 1);
                    writer.WriteLine(name);
            }
               
            
            catch (Exception)
            {
                    throw;
            }
            writer.Close();
            Close();

        }

        private void set_url(object sender, EventArgs e)
        {
            FolderBrowserDialog diag = new FolderBrowserDialog();
            if (diag.ShowDialog() == System.Windows.Forms.DialogResult.OK)
            {
                string file_url = diag.SelectedPath;  //selected folder path
                txt_url.Text = file_url;
            }
        }
    }
}
