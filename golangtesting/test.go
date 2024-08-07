package main

import (
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
)

const (
	logFilePerm = 0666
)

func main() {
	logFile, err := os.OpenFile("errors.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, logFilePerm)
	if err != nil {
		log.Fatalf("failed to open log file: %v", err)
	}
	defer logFile.Close()
	log.SetOutput(logFile)

	wd, err := os.Getwd()
	if err != nil {
		log.Fatal(err)
	}

	dirPath := wd

	jsonFiles, err := filepath.Glob(filepath.Join(dirPath, "*.json"))
	if err != nil {
		log.Fatal(err)
	}

	for _, file := range jsonFiles {
		base := filepath.Base(file)
		fileName := strings.TrimSuffix(base, filepath.Ext(base))

		jsonFile, err := os.Open(file)
		if err != nil {
			log.Errorf("error opening file %s: %v", file, err)
			continue
		}
		defer jsonFile.Close()

		hash, err := hashFile(jsonFile)
		if err != nil {
			log.Errorf("error hashing file %s: %v", file, err)
			continue
		}

		outputFile, err := os.Create(filepath.Join(dirPath, fileName+".sha256"))
		if err != nil {
			log.Errorf("error creating output file for %s: %v", file, err)
			continue
		}
		defer outputFile.Close()

		_, err = outputFile.Write(hash)
		if err != nil {
			log.Errorf("error writing to output file for %s: %v", file, err)
			continue
		}

		log.Infof("hashed file %s and saved to %s", base, outputFile.Name())
	}

	files, err := filepath.Glob(filepath.Join(dirPath, "*.sha256"))
	if err != nil {
		log.Fatal(err)
	}

	numbers := make([]int, 0, len(files))
	for _, file := range files {
		base := filepath.Base(file)
		ext := filepath.Ext(base)
		numStr := strings.TrimSuffix(base, ext)
		num, err := strconv.Atoi(numStr)
		if err != nil {
			log.Errorf("error parsing file name %s: %v", file, err)
			continue
		}
		numbers = append(numbers, num)
	}

	sort.Ints(numbers)

	maxNum := numbers[len(numbers)-1]

	for i := 1; i <= maxNum; i++ {
		fileName := fmt.Sprintf("%d.sha256", i)
		log.Infof("hashed file %s", fileName)
	}
}

func hashFile(file io.Reader) ([]byte, error) {
	hash := sha256.New()
	_, err := io.Copy(hash, file)
	if err != nil {
		return nil, err
	}
	return hash.Sum(nil), nil
}