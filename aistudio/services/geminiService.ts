
import { GoogleGenAI, Type } from "@google/genai";
import { ICDResult } from '../types';

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  throw new Error("API_KEY environment variable not set");
}

const ai = new GoogleGenAI({ apiKey: API_KEY });

const responseSchema = {
    type: Type.ARRAY,
    items: {
      type: Type.OBJECT,
      properties: {
        code: {
          type: Type.STRING,
          description: "The official ICD-10 code (e.g., 'J45.909').",
        },
        description: {
          type: Type.STRING,
          description: "The detailed clinical description of the code.",
        },
        category: {
          type: Type.STRING,
          description: "A broader clinical category for the code (e.g., 'Respiratory Diseases').",
        },
      },
      required: ["code", "description", "category"],
    },
};

export const fetchICDCodes = async (query: string): Promise<ICDResult[]> => {
  const prompt = `
    You are a highly-trained medical coding assistant. Your task is to find relevant ICD-10 codes based on a user's search query.
    Return a list of the most relevant codes. For each code, provide the official ICD-10 code, a detailed description, and a general category.
    
    Search Query: "${query}"
  `;

  try {
    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: prompt,
      config: {
        responseMimeType: "application/json",
        responseSchema: responseSchema,
        temperature: 0.2,
      },
    });

    const jsonText = response.text.trim();
    if (!jsonText) {
        return [];
    }
    
    const parsedResults: ICDResult[] = JSON.parse(jsonText);
    return parsedResults;

  } catch (error) {
    console.error("Error fetching ICD codes from Gemini:", error);
    if (error instanceof Error && error.message.includes('SAFETY')) {
        throw new Error("The query was blocked due to safety settings. Please try a different search term.");
    }
    throw new Error("Failed to retrieve ICD codes. The model may be unavailable or the query is invalid.");
  }
};
