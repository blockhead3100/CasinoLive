/**
 * Generates a random number within a specified range.
 *
 * @param min The minimum value of the range (inclusive).
 * @param max The maximum value of the range (inclusive).
 * @returns A random number between min and max.
 */
export async function generateRandomNumber(min: number, max: number): Promise<number> {
  // TODO: Implement this by calling an API.

  return Math.floor(Math.random() * (max - min + 1)) + min;
}
