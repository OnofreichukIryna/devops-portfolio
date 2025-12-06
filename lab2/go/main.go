package main

import (
	"flag"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// Categories for sorting
var extensions = map[string]string{
	".jpg": "Images", ".png": "Images", ".jpeg": "Images",
	".pdf": "Documents", ".txt": "Documents", ".docx": "Documents",
	".mp4": "Videos", ".mov": "Videos",
	".mp3": "Music",
	".zip": "Archives", ".tar": "Archives", ".gz": "Archives",
}

func main() {
	// CLI flags
	dirPath := flag.String("path", ".", "Path to directory")
	dryRun := flag.Bool("dry-run", false, "Show output without moving files")
	flag.Parse()

	files, err := os.ReadDir(*dirPath)
	if err != nil {
		fmt.Println("Error reading directory:", err)
		os.Exit(1)
	}

	fmt.Printf("Sorting files in: %s\n", *dirPath)

	for _, file := range files {
		// Skip folders and the script itself
		if file.IsDir() || file.Name() == "main.go" || file.Name() == "go.mod" {
			continue
		}

		ext := strings.ToLower(filepath.Ext(file.Name()))
		targetFolder := "Others"
		
		if val, ok := extensions[ext]; ok {
			targetFolder = val
		}

		fullTargetDir := filepath.Join(*dirPath, targetFolder)
		srcPath := filepath.Join(*dirPath, file.Name())
		dstPath := filepath.Join(fullTargetDir, file.Name())

		if *dryRun {
			fmt.Printf("[DRY-RUN] Move %s -> %s\n", file.Name(), targetFolder)
		} else {
			// Ensure folder exists
			os.MkdirAll(fullTargetDir, 0755)
			
			err := os.Rename(srcPath, dstPath)
			if err != nil {
				fmt.Printf("Error moving %s: %v\n", file.Name(), err)
			} else {
				fmt.Printf("Moved: %s -> %s\n", file.Name(), targetFolder)
			}
		}
	}
}