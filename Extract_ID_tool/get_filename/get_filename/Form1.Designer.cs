namespace get_filename
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.txt1 = new System.Windows.Forms.TextBox();
            this.openfd = new System.Windows.Forms.Button();
            this.export_csv = new System.Windows.Forms.Button();
            this.txt_url = new System.Windows.Forms.TextBox();
            this.btn_url = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // txt1
            // 
            this.txt1.Location = new System.Drawing.Point(12, 96);
            this.txt1.Name = "txt1";
            this.txt1.Size = new System.Drawing.Size(200, 20);
            this.txt1.TabIndex = 0;
            // 
            // openfd
            // 
            this.openfd.Location = new System.Drawing.Point(229, 93);
            this.openfd.Name = "openfd";
            this.openfd.Size = new System.Drawing.Size(171, 23);
            this.openfd.TabIndex = 1;
            this.openfd.Text = "open your marking folder";
            this.openfd.UseVisualStyleBackColor = true;
            this.openfd.Click += new System.EventHandler(this.openfolder);
            // 
            // export_csv
            // 
            this.export_csv.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.export_csv.Location = new System.Drawing.Point(113, 151);
            this.export_csv.Name = "export_csv";
            this.export_csv.Size = new System.Drawing.Size(166, 30);
            this.export_csv.TabIndex = 2;
            this.export_csv.Text = "Export to CSV";
            this.export_csv.UseVisualStyleBackColor = true;
            this.export_csv.Click += new System.EventHandler(this.export_to_csv);
            // 
            // txt_url
            // 
            this.txt_url.Location = new System.Drawing.Point(12, 42);
            this.txt_url.Name = "txt_url";
            this.txt_url.Size = new System.Drawing.Size(198, 20);
            this.txt_url.TabIndex = 3;
            // 
            // btn_url
            // 
            this.btn_url.Location = new System.Drawing.Point(229, 42);
            this.btn_url.Name = "btn_url";
            this.btn_url.Size = new System.Drawing.Size(171, 24);
            this.btn_url.TabIndex = 4;
            this.btn_url.Text = "set url of your csv file";
            this.btn_url.UseVisualStyleBackColor = true;
            this.btn_url.Click += new System.EventHandler(this.set_url);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(410, 261);
            this.Controls.Add(this.btn_url);
            this.Controls.Add(this.txt_url);
            this.Controls.Add(this.export_csv);
            this.Controls.Add(this.openfd);
            this.Controls.Add(this.txt1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox txt1;
        private System.Windows.Forms.Button openfd;
        private System.Windows.Forms.Button export_csv;
        private System.Windows.Forms.TextBox txt_url;
        private System.Windows.Forms.Button btn_url;
    }
}

