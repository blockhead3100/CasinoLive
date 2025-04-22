// The AI flow to personalize game recommendations based on user preferences.
//
// - personalizeGameRecommendations - A function that handles the game recommendation process.
// - PersonalizeGameRecommendationsInput - The input type for the personalizeGameRecommendations function.
// - PersonalizeGameRecommendationsOutput - The return type for the personalizeGameRecommendations function.

'use server';

import {ai} from '@/ai/ai-instance';
import {z} from 'genkit';

const PersonalizeGameRecommendationsInputSchema = z.object({
  userHistory: z.string().describe('The user history including games played, bet sizes, and time spent on each game.'),
  availableGames: z.string().describe('A list of available games with descriptions and difficulty levels.'),
});
export type PersonalizeGameRecommendationsInput = z.infer<typeof PersonalizeGameRecommendationsInputSchema>;

const PersonalizeGameRecommendationsOutputSchema = z.object({
  recommendedGame: z.string().describe('The name of the recommended game.'),
  difficultyLevel: z.string().describe('The recommended difficulty level (e.g., easy, medium, hard).'),
  reason: z.string().describe('Explanation of why the game and difficulty level were recommended.'),
});
export type PersonalizeGameRecommendationsOutput = z.infer<typeof PersonalizeGameRecommendationsOutputSchema>;

export async function personalizeGameRecommendations(input: PersonalizeGameRecommendationsInput): Promise<PersonalizeGameRecommendationsOutput> {
  return personalizeGameRecommendationsFlow(input);
}

const prompt = ai.definePrompt({
  name: 'personalizeGameRecommendationsPrompt',
  input: {
    schema: z.object({
      userHistory: z.string().describe('The user history including games played, bet sizes, and time spent on each game.'),
      availableGames: z.string().describe('A list of available games with descriptions and difficulty levels.'),
    }),
  },
  output: {
    schema: z.object({
      recommendedGame: z.string().describe('The name of the recommended game.'),
      difficultyLevel: z.string().describe('The recommended difficulty level (e.g., easy, medium, hard).'),
      reason: z.string().describe('Explanation of why the game and difficulty level were recommended.'),
    }),
  },
  prompt: `You are an expert in personalized game recommendations. Analyze the user's game history and suggest a game and difficulty level that they would enjoy.

User History: {{{userHistory}}}
Available Games: {{{availableGames}}}

Based on this information, recommend a game and difficulty level, and explain why it would be a good fit for the user.

Consider suggesting games of increased difficulty if the user has been winning a lot. If the user has been losing, suggest an easier difficulty level.
`,
});

const personalizeGameRecommendationsFlow = ai.defineFlow<
  typeof PersonalizeGameRecommendationsInputSchema,
  typeof PersonalizeGameRecommendationsOutputSchema
>({
  name: 'personalizeGameRecommendationsFlow',
  inputSchema: PersonalizeGameRecommendationsInputSchema,
  outputSchema: PersonalizeGameRecommendationsOutputSchema,
}, async input => {
  const {output} = await prompt(input);
  return output!;
});
