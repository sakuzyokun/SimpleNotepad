using System;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace SimpleNotepad
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void OpenFile(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                textBox1.Text = File.ReadAllText(ofd.FileName);
            }
            ofd.Dispose();
        }

        private void SaveFile(object sender, EventArgs e)
        {
            SaveFileDialog sfd = new SaveFileDialog();
            if (sfd.ShowDialog() == DialogResult.OK)
            {
                File.WriteAllText(sfd.FileName, textBox1.Text);
            }
            sfd.Dispose();
        }

        private void ChangeFont(object sender, EventArgs e)
        {
            using (FontDialog fd = new FontDialog())
            {
                fd.Font = textBox1.Font;
                if (fd.ShowDialog() == DialogResult.OK)
                {
                    textBox1.Font = fd.Font;
                    UpdateStatus(null, null); // ステータスバー更新
                }
            }
        }

        private void UpdateStatus(object sender, EventArgs e)
        {
            int totalLines = textBox1.Lines.Length;
            int totalChars = textBox1.Text.Length;
            int currentLine = textBox1.GetLineFromCharIndex(textBox1.SelectionStart) + 1;
            int currentChar = textBox1.SelectionStart + 1;

            string fontInfo = $"{textBox1.Font.Name}, {textBox1.Font.Size}pt";

            statusLabel.Text = string.Format(
                "行数: {0} | 選択行: {1} | 文字数: {2} | カーソル位置: {3} | フォント: {4}",
                totalLines, currentLine, totalChars, currentChar, fontInfo);
        }

        private void ShowVersionInfo(object sender, EventArgs e)
        {
            Form infoForm = new Form()
            {
                Text = "バージョン情報",
                Size = new Size(300, 200),
                FormBorderStyle = FormBorderStyle.FixedDialog,
                MaximizeBox = false,
                MinimizeBox = false,
                StartPosition = FormStartPosition.CenterParent
            };

            Label title = new Label()
            {
                Text = "SimpleNotepad",
                Font = new Font("MS UI Gothic", 14, FontStyle.Bold),
                AutoSize = true,
                Location = new Point(10, 10)
            };

            Label detail = new Label()
            {
                Text = "Version: 1.0.0\n作者: 削除くん",
                Font = new Font("MS UI Gothic", 9),
                AutoSize = true,
                Location = new Point(10, 50)
            };

            infoForm.Controls.Add(title);
            infoForm.Controls.Add(detail);
            infoForm.ShowDialog();
        }
    }
}
