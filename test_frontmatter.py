import frontmatter

# Test B0F3KHSF4V
post = frontmatter.load('./shop/B0F3KHSF4V.md')
print("B0F3KHSF4V:")
print(f"  link: {post.get('link')}")
print(f"  amazonLink: {post.get('amazonLink')}")
print(f"  permalink: {post.get('permalink')}")
print()

# Test B0FJ7K4G48
post2 = frontmatter.load('./shop/B0FJ7K4G48.md')
print("B0FJ7K4G48:")
print(f"  link: {post2.get('link')}")
print(f"  amazonLink: {post2.get('amazonLink')}")
print(f"  permalink: {post2.get('permalink')}")
